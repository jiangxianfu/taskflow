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
from taskflowdb import TaskFlowDB

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def main(flow_instance_id):
    try:
        taskflowdb = TaskFlowDB()
        # print("task_flow_id:%d" % flow_instance_id)

        # 获取基础数据信息
        instance_data = taskflowdb.get_instance(flow_instance_id)
        flow_id = instance_data["flowid"]
        step_num = instance_data["curstepnum"]
        flow_step_data = taskflowdb.get_flow_step(flow_id, step_num)

        module = flow_step_data["modulename"]

        # 动态导入运行模块
        inner_module = importlib.import_module("modules.%s" % module)
        inner_method = getattr(inner_module, "main")

        # 处理参数数据
        inner_kwargs = {"id": ""}

        # 运行模块
        ret = inner_method(**inner_kwargs)
        result = True
        message = ""
        if ret:
            result = ret[0]
            message = str(ret[1])
        print(result, message)
    except Exception as ex:
        print("err", ex)


if __name__ == '__main__':
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
