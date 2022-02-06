# -*- coding: utf-8 -*-
"""
author: jiangxf
date: 2020-01-29
description: 该方法主要是用于启动整个工作流程序

    #动态加载module
    #判断module属于action还是check
    #根据结果判断流程允许情况
    #if判断当前task是否成功,
       如果是workflow则：
          #创建任务更新下个任务的状态
          #if end
        #更新任务
    #else
        #更新任务

"""

import sys
import importlib
import getopt
import logging
import json
import traceback
from contrib.taskflowdb import TaskFlowDB
from contrib.redisdb import RedisDB
from contrib.utils import CustomJSONEncoder
from contrib.workflow_spec import WorkflowSpec
import inspect

logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(asctime)s - %(levelname)s - %(message)s')


def update_source_task_status(db: TaskFlowDB, source_type: str, source_id: int, status: str):
    if source_type == "schedule":
        db.update_sched("end", source_id, status)
    elif source_type == "form":
        db.save_taskform_status(source_id, status)


def parse_args_json_str(db: TaskFlowDB, instance_id: int):
    data = {}
    return json.dumps(data, cls=CustomJSONEncoder)


def main(instance_id: int):
    """
    当前运行的一定是module
    """
    try:
        taskflowdb = TaskFlowDB()
        # 获取基础数据信息
        instance_data = taskflowdb.get_instance(instance_id)
        if "module" != instance_data["task_type"]:
            logging.error("当前运行的不是模块!")
            raise ValueError("id %s is not module" % instance_id)
        module_name = instance_data["task_name"]
        # 动态导入运行模块
        inner_func = importlib.import_module("modules.%s" % module_name)
        inner_func_main = getattr(inner_func, "main")
        # 实例获取到的参数
        inner_func_main_full_arg_spec = inspect.getfullargspec(inner_func_main)
        inner_func_main_argument_list = inner_func_main_full_arg_spec.args
        # 处理参数数据
        # 运行中的产生的参数
        inner_func_kwargs = {}
        # 处理输入参数别名的情况并设定模块运行数据
        input_arguments = json.loads(instance_data["args_json"])
        for arg_name in inner_func_main_argument_list:
            if arg_name in input_arguments:
                arg_value = input_arguments.get(arg_name)
                inner_func_kwargs[arg_name] = arg_value
        if inner_func_main_full_arg_spec.varkw:
            inner_func_kwargs["sys_instance"] = instance_data
        # 暂时关闭释放资源,因为连接串资源宝贵
        taskflowdb.close()
        # 运行模块
        success = True
        message = ""
        return_data = {}
        run_result = None
        try:
            logging.info("----------run module: %s start----------" % module_name)
            run_result = inner_func_main(**inner_func_kwargs)
            logging.info("----------run module: %s finish----------" % module_name)
            if run_result is not None:
                if type(run_result) is bool:
                    success = run_result
                elif type(run_result) is tuple:
                    len_ret = len(run_result)
                    if len_ret > 0:
                        success = bool(run_result[0])
                    if len_ret > 1:
                        message = str(run_result[1])
                    if len_ret > 2:
                        return_data = dict(run_result[2])
        except:
            success = False
            message = traceback.format_exc()
            logging.error("run module err \n %s", message)
        redisdb = RedisDB()
        if str(module_name).startswith("check_"):
            if run_result is None:
                # 这里需要出来下check的功能
                data = redisdb.get_check_hash(instance_id)
                times = int(data) if data else 0
                redisdb.set_check_hash(instance_id, times + 1)
                return
            else:
                redisdb.del_check_hash(instance_id)
        result_status = 'success' if success else 'failure'
        # 重新开启db资源
        taskflowdb = TaskFlowDB()
        # 更新instance 数据
        result_json = json.dumps(return_data, cls=CustomJSONEncoder)
        taskflowdb.save_instance_status(instance_id, result_status, result_message=message, result_json=result_json)
        # 处理执行结果
        # 如果是工作流
        source_id = instance_data["source_id"]
        source_type = instance_data["source_type"]
        parent_id = instance_data["parent_id"]
        if parent_id > 0:
            parent_instance = taskflowdb.get_instance(parent_id)
            workflow_name = parent_instance["task_name"]
            wf = WorkflowSpec(workflow_name)
            cur_step_name = instance_data["name"]
            if cur_step_name == wf.end:
                update_source_task_status(taskflowdb, source_type, source_id, result_status)
                return
            cur_step = wf.steps[cur_step_name]
            if success:
                next_step_name = cur_step.get("on-success")
            else:
                taskflowdb.save_instance_status(parent_id, result_status, result_message=message)
                next_step_name = cur_step.get("on-failure")
            if not next_step_name:
                update_source_task_status(taskflowdb, source_type, source_id, result_status)
                return
            # 计算获取下一步骤的参数数据
            next_module_name = wf.steps[next_step_name].get("module")
            next_step_args_json = wf.get_step_parameters(instance_id, next_step_name, True)
            next_instance_id = taskflowdb.create_instance(next_step_name, source_id, source_type, parent_id,
                                                          "module", next_module_name, next_step_args_json, 'running')
            redisdb.push_run_queue(next_instance_id)
        else:
            update_source_task_status(taskflowdb, source_type, source_id, result_status)
    except:
        logging.error("task run err \n %s", traceback.format_exc())


if __name__ == '__main__':
    opts = []
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:", ["id="])
    except getopt.GetoptError:
        print("args are error, please use task_run.py -h.")
    instance_id = 0
    help_info = "usage: task_run.py -i <task_instance_id>"
    if len(opts) > 0:
        for opt, arg in opts:
            if opt == "-h":
                print(help_info)
            elif opt in ("-i", "--id"):
                instance_id = int(arg)
        if instance_id > 0:
            main(instance_id)
        else:
            print(help_info)
    else:
        print(help_info)
