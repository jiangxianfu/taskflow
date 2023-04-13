# -*- coding: utf-8 -*-
"""
author: jiangxf
date: 2020-01-29
description: 该方法主要是用于启动整个工作流程序

#从消息队列中消费任务
    #并执行任务 task_run.py
"""

import time
import subprocess
from core.redisdb import RedisDB
from core.taskflowdb import TaskFlowDB
import socket
from core import settings
import logging
import traceback
import sys

logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(asctime)s - %(levelname)s - %(message)s')


def message_process(instance_id):
    try:
        # 获取需要运行的模块
        task_run_file = "task_run.py"
        output_filename = settings.TASK_RUN_LOG_FORMAT % instance_id
        logging.debug("output_filename:%s", output_filename)
        logging.debug("task_run_filename:%s", task_run_file)
        logging.debug("task python bin location:%s", settings.PYTHONBIN)
        with open(output_filename, "a") as outfile:
            pm = subprocess.Popen([settings.PYTHONBIN, "-u", task_run_file, "-i", str(instance_id)],
                                  close_fds=True,
                                  cwd=settings.BASE_DIR,
                                  stdout=outfile, stderr=subprocess.STDOUT)
            taskflowdb = TaskFlowDB()
            worker_hostname = socket.gethostname()
            worker_pid = pm.pid
            taskflowdb.save_instance_status(instance_id, 'running', worker_hostname=worker_hostname,
                                            worker_pid=worker_pid)
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
