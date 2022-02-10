# -*- coding:utf-8 -*-

"""
    # 1.获取有效状态下的cron
    type: workflow,module
    # 2. 判断是workflow还是module
    # 3. 根据python_code获取参数
    create task type,status,param
    if is workflow:
        create task,status, param,parent_id=task_id
    update sched

"""

import time
import traceback
import sys
import logging
from croniter import croniter
import datetime
from contrib.taskflowdb import TaskFlowDB
from contrib.redisdb import RedisDB
from contrib.workflow_spec import WorkflowSpec
from contrib.utils import CustomJSONEncoder
import json

logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(asctime)s - %(levelname)s - %(message)s')


def get_arguments(python_code, run_time, to_json=False):
    """
    直接跑代码
    """
    ns = {}
    exec(python_code.encode('utf8'), ns)
    kwargs = {"run_time": run_time}
    data = ns["get_arguments"](**kwargs)
    if to_json:
        data = json.dumps(data, ensure_ascii=False, cls=CustomJSONEncoder)
    return data


def main():
    taskflowdb = TaskFlowDB()
    redisdb = RedisDB()
    while True:
        # 找到当前调度中有效调度,活动状态,有效数据
        data = taskflowdb.get_sched_cron()
        if len(data) == 0:
            time.sleep(30)
            continue
        for item in data:
            try:
                # 精确到秒
                trigger_time = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                          '%Y-%m-%d %H:%M:%S')
                cron = croniter(item["cron_sched"], trigger_time)
                args_python_code = item["args_python_code"]
                args_json = get_arguments(args_python_code, trigger_time, True)

                # 默认没有父任务
                parent_id = 0
                source_id = item["id"]
                source_type = "schedule"
                if "workflow" == item["task_type"]:
                    # 则先创建父任务
                    instance_id = taskflowdb.create_instance(item["task_name"], source_id, source_type, parent_id,
                                                             "workflow", item["task_name"], args_json,
                                                             'running')
                    wf = WorkflowSpec(item["task_name"], taskflowdb, instance_id, parent_id)
                    step_name = wf.begin_step
                    module_name = wf.steps[wf.begin_step].get("module")
                    args_json = wf.get_next_step_parameters(step_name, True)
                    parent_id = instance_id
                elif "module" == item["task_type"]:
                    module_name = item["task_name"]
                    step_name = module_name
                else:
                    raise ValueError("task_type is invalid")
                instance_id = taskflowdb.create_instance(step_name, source_id, source_type, parent_id,
                                                         "module", module_name, args_json, 'running')

                trigger_next_time = cron.get_next(datetime.datetime)
                redisdb.push_run_queue(instance_id)
                taskflowdb.update_sched("start", item["id"], 'running',
                                        trigger_last_time=trigger_time,
                                        trigger_next_time=trigger_next_time)
                logging.info("shcedid=%s is running" % (item["id"]))
            except:
                logging.error(traceback.format_exc())
        time.sleep(3)


if __name__ == '__main__':
    main()
