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
import psutil
import subprocess
from core import settings
from core.redisdb import RedisDB
from core.taskflowdb import TaskFlowDB

logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(asctime)s - %(levelname)s - %(message)s')
task_run_file = "%s/task_run.py" % os.path.dirname(os.path.abspath(__file__))


def check_run():
    memory = psutil.virtual_memory()
    if memory.percent > 80:
        logging.warning("waiting, memory usage: %s" % repr(memory))
        time.sleep(30)
        return False
    _, data = subprocess.getstatusoutput("ps -ef|grep '%s -i '|wc -l" % task_run_file)
    process_list_count = int(data.strip()) - 2
    if process_list_count > 100:
        logging.warning("waiting, process count: %s, can't do task." % process_list_count)
        time.sleep(30)
        return False
    logging.info('process count:%s,can do task.', process_list_count)
    return True


def message_process(instance_id):
    try:
        # 获取需要运行的模块
        output_filename = settings.TASK_RUN_LOG_FORMAT % instance_id
        os.system("nohup %s -u %s %s >%s 2>&1 &" % (settings.PYTHONBIN, task_run_file, instance_id, output_filename))
        logging.info("task_run instance:%s" % instance_id)
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
        if check_run():
            data = redisdb.pop_run_queue()
            if data is not None:
                message_process(int(data))
            time.sleep(1)


if __name__ == '__main__':
    main()
