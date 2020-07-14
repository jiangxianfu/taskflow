# -*- coding: utf-8 -*-
"""
author: jiangxf
date: 2020-01-29
description: 该方法主要是用于启动整个工作流程序

"""

import sys
import importlib
import getopt
import logging
import json
from taskflowdb import TaskFlowDB
from redisdb import RedisDB
import datetime
import traceback
import socket
from com.daemonize import daemonize
from com.utils import CustomJSONEncoder

logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(asctime)s - %(levelname)s - %(message)s')


def main(flow_instance_id):
    try:
        taskflowdb = TaskFlowDB()
        # 获取基础数据信息
        instance_data = taskflowdb.get_instance(flow_instance_id)
        flow_id = instance_data["flowid"]
        step_num = instance_data["curstepnum"]
        flow_step_data = taskflowdb.get_flow_step(flow_id, step_num)

        module_name = flow_step_data["modulename"]

        module_data = taskflowdb.get_module(module_name)
        arguments_definition = json.loads(module_data["arguments"])

        # 动态导入运行模块
        inner_module = importlib.import_module("modules.%s" % module_name)
        inner_method = getattr(inner_module, "main")

        # 处理参数数据
        # 实例获取到的参数
        dict_instance_arguments = json.loads(instance_data["arguments"])
        # 运行中的产生的参数
        dict_instance_run_data = taskflowdb.get_instance_run_data(flow_instance_id)
        inner_kwargs = {}

        # 处理输入参数别名的情况并设定模块运行数据
        input_argment_alias = json.loads(flow_step_data["inputargalias"])
        for arg_item in arguments_definition:
            key_name = arg_item["name"]
            input_key_name = input_argment_alias.get(key_name, key_name)
            if key_name in dict_instance_arguments:
                inner_kwargs[key_name] = dict_instance_arguments.get(input_key_name)
            elif key_name in dict_instance_run_data:
                inner_kwargs[key_name] = dict_instance_run_data.get(input_key_name)
            else:
                inner_kwargs[key_name] = None
        inner_kwargs["sys_taskflow_instance"] = instance_data

        # 记录instance_steps数据
        step_name = flow_step_data["stepname"]
        json_data = json.dumps(inner_kwargs, cls=CustomJSONEncoder)
        worker_name = socket.gethostname()
        instance_step_id = taskflowdb.add_instance_step(flow_instance_id, step_num, step_name, json_data, worker_name,
                                                        'running', '')

        # 暂时关闭释放资源,因为连接串资源宝贵
        taskflowdb.close()
        # 运行模块
        result = True
        message = ""
        return_data = {}
        try:
            ret = inner_method(**inner_kwargs)
            if ret and type(ret) is tuple:
                len_ret = len(ret)
                if len_ret > 0:
                    result = bool(ret[0])
                if len_ret > 1:
                    message = str(ret[1])
                if len_ret > 2:
                    return_data = dict(ret[2])
        except:
            result = False
            message = traceback.format_exc()
            logging.error("run module err \n %s", message)
        exec_status = u'success' if result else u'fail'
        # 重新开启db资源
        taskflowdb = TaskFlowDB()
        # 更新instance_steps 数据
        taskflowdb.save_instance_step_status(instance_step_id, exec_status, message)
        # 处理执行结果
        if result:
            # 执行成功
            # 参数别名处理与运行数据保存
            output_argment_alias = json.loads(flow_step_data["outputargalias"])
            for key, value in return_data.items():
                new_key_name = output_argment_alias.get(key, key)
                new_value = value
                if type(value) in [tuple, set]:
                    new_value = list(value)
                if type(value) in [list, set, dict, tuple]:
                    key_type = 'object'
                else:
                    key_type = 'simple'
                if 'object' == key_type:
                    new_value = json.dumps(new_value, cls=CustomJSONEncoder)
                taskflowdb.set_instance_run_data(flow_instance_id, key_type, new_key_name, new_value)
            # 是否整个流程结束
            if step_num >= instance_data["stepcount"]:
                taskflowdb.save_instance_status(flow_instance_id, exec_status)
            else:
                # 下个步骤是否需要暂停
                nextstep_waitseconds = int(flow_step_data["nextstep_waitseconds"])
                curstepnum = step_num + 1
                curstepruncount = 0
                if nextstep_waitseconds == -1:
                    exec_status = 'pause'
                    next_runtime = datetime.datetime.now()
                else:
                    exec_status = 'standby'
                    # 加入 next step 延迟执行逻辑
                    next_runtime = datetime.datetime.now() + datetime.timedelta(seconds=nextstep_waitseconds)
                taskflowdb.save_instance_status(flow_instance_id, exec_status,
                                                curstepnum, curstepruncount, next_runtime)
        else:
            # 如果执行失败，则判断是否继续执行重试
            failed_retrycounts = int(flow_step_data["failed_retrycounts"])
            curstepruncount = int(instance_data["curstepruncount"]) + 1
            # 如果不重试 或者 超过重试次数
            if failed_retrycounts == 0 or curstepruncount > failed_retrycounts:
                taskflowdb.save_instance_status(flow_instance_id, exec_status, cur_step_runcount=curstepruncount)
            else:
                exec_status = 'standby'
                # 默认一分钟后重试
                next_runtime = datetime.datetime.now() + datetime.timedelta(seconds=60)
                taskflowdb.save_instance_status(flow_instance_id, exec_status, cur_step_runcount=curstepruncount,
                                                next_runtime=next_runtime)
    except:
        logging.error("task run err \n %s", traceback.format_exc())
    try:
        # remove running flow_instance_id
        redisdb = RedisDB()
        redisdb.remove_running_instance(flow_instance_id)
        redisdb.close()
    except:
        logging.error("task run remove redis running key err \n %s", traceback.format_exc())


if __name__ == '__main__':
    # run as background
    daemonize()
    opts = []
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:", ["id="])
    except getopt.GetoptError:
        print("args are error, please use task_run.py -h.")
    task_flow_id = 0
    help_info = "usage: task_run.py -i <task_flow_id>"
    if len(opts) > 0:
        for opt, arg in opts:
            if opt == "-h":
                print(help_info)
            elif opt in ("-i", "--id"):
                task_flow_id = int(arg)
        if task_flow_id > 0:
            main(task_flow_id)
        else:
            print(help_info)
    else:
        print(help_info)
