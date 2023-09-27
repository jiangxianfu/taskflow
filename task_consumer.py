# -*- coding: utf-8 -*-
"""
author: jiangxf
date: 2020-01-29
description: 该方法主要是用于启动整个工作流程序

#从消息队列中消费任务
    #并执行任务 task_run.py
"""

import time
import logging
import traceback
import sys
import os
import socket
from core import settings
from core.redisdb import RedisDB
from core.taskflowdb import TaskFlowDB

logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(asctime)s - %(levelname)s - %(message)s')


def message_process(instance_id):
    try:
        # 获取需要运行的模块
        task_run_file = "task_run.py"
        output_filename = settings.TASK_RUN_LOG_FORMAT % instance_id
        logging.debug("output_filename:%s", output_filename)
        logging.debug("task_run_filename:%s", task_run_file)
        logging.debug("task python bin location:%s", settings.PYTHONBIN)
        os.system("nohup %s -u %s %s >%s 2>&1 &" % (settings.PYTHONBIN, task_run_file, instance_id, output_filename))
        taskflowdb = TaskFlowDB()
        worker_hostname = socket.gethostname()
        taskflowdb.save_instance_status(instance_id, 'running', worker_hostname=worker_hostname)
    except:
        logging.error('message_process err \n %s', traceback.format_exc())


def main():
    logging.info("taskflow receiver is running")
    # get redis data
    redisdb = RedisDB()
    while True:
        data = redisdb.pop_run_queue()
        if data is not None:
            message_process(int(data))
        time.sleep(1)


if __name__ == '__main__':
    main()
