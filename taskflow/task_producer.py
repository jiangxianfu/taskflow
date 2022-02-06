# -*- coding: utf-8 -*-
"""
author: jiangxf
date: 2020-01-29
description: 该方法主要是用于启动整个工作流程序


# 获取待运行的任务
# 判断是否是workflow或module
# 创建任务
# 发送到消息队列
# 分配任务到消息队列中

"""

import time
import logging
from contrib.redisdb import RedisDB
from contrib.taskflowdb import TaskFlowDB
from contrib.workflow_spec import WorkflowSpec
import sys
import traceback

logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    logging.info("taskflow producer is running")
    taskflowdb = TaskFlowDB()
    redisdb = RedisDB()
    while True:
        data = taskflowdb.get_undo_taskforms()
        if len(data) == 0:
            time.sleep(30)
            continue
        for item in data:
            try:
                source_id = item["id"]
                source_type = "form"
                # 默认没有父任务
                parent_id = 0
                if "workflow" == item["task_type"]:
                    # 则先创建父任务
                    parent_id = taskflowdb.create_instance(item["task_name"], source_id, source_type, parent_id,
                                                           "workflow", item["task_name"], item["args_json"],
                                                           'running')
                    wf = WorkflowSpec(item["task_name"])
                    step_name = wf.begin_step
                    module_name = wf.steps[step_name].get("module")
                    args_json = wf.get_step_parameters(taskflowdb,parent_id, step_name, True)
                elif "module" == item["task_type"]:
                    module_name = item["task_name"]
                    step_name = module_name
                    args_json = item["args_json"]
                else:
                    raise ValueError("task_type is invalid")
                # 创建任务
                instance_id = taskflowdb.create_instance(step_name, source_id, source_type, parent_id,
                                                         "module", module_name, args_json, 'running')
                redisdb.push_run_queue(instance_id)
                taskflowdb.save_taskform_status(item["id"], 'running')
            except:
                logging.error(traceback.format_exc())
        time.sleep(3)


if __name__ == '__main__':
    main()
