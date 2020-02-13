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
from com.dbhelper import DBHelper
from com.dbconfig import connect_short
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')



def main(flow_instance_id):
    try:
        print("task_flow_id:%d" % flow_instance_id)
        db = DBHelper(connect_short(""))
        data = db.query("select * from flow_instance where id =%s" % flow_instance_id)
        step_num = data["step_num"]
        data2 = db.query("select * from flow_steps where flow_id=%s and step_num=%s", (flow_instance_id,step_num))
        module = data2["module_name"]
        inner_module = importlib.import_module("modules.%s" % module)
        inner_method = getattr(inner_module, "main")
        inner_kwargs = {"id": ""}
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
