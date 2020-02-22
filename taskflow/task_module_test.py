# -*- coding: utf-8 -*-
"""
author: jiangxf
date: 2020-01-29
description: 该方法主要是用于单独运行模块的测试功能

"""

import sys
import importlib
import getopt
import logging
import traceback

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main(module_name):
    try:
        # 动态导入运行模块
        inner_module = importlib.import_module("modules.%s" % module_name)
        inner_method = getattr(inner_module, "test_main")
        inner_kwargs = {}
        # init sys empty instance
        inner_kwargs["sys_taskflow_instance"] = {}
        try:
            ret = inner_method(**inner_kwargs)
            print("module return data:", ret)
        except:
            logging.error("run module err \n %s", traceback.format_exc())
    except:
        logging.error("task run module err \n %s", traceback.format_exc())


if __name__ == '__main__':
    opts = []
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hm:", ["module="])
    except getopt.GetoptError:
        print("args are error, please use task_module_test.py -h.")
    module_name = ""
    help_info = "usage: task_module_test.py -m <module_name>"
    if len(opts) > 0:
        for opt, arg in opts:
            if opt == "-h":
                print(help_info)
            elif opt in ("-m", "--module"):
                module_name = arg
        if len(module_name) > 0:
            main(module_name)
        else:
            print(help_info)
    else:
        print(help_info)
