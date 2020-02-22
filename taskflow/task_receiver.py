# -*- coding: utf-8 -*-
"""
author: jiangxf
date: 2020-01-29
description: 该方法主要是用于启动整个工作流程序

"""

import time
import os
import subprocess
from redisdb import RedisDB
import socket
import settings
import logging
import traceback
import sys

logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(asctime)s - %(levelname)s - %(message)s')


def message_process(flow_instance_id):
    try:
        redisdb = RedisDB()
        # 获取需要运行的模块
        output_filename = settings.TASK_RUN_LOG_FORMAT % flow_instance_id
        logging.debug("output_filename:%s", output_filename)
        logging.debug("task_run_filename:%s", settings.TASK_RUN_FILE)
        logging.debug("task python bin location:%s", settings.PYTHONBIN)
        with open(output_filename, "a") as outfile:
            pm = subprocess.Popen([settings.PYTHONBIN, "-u", settings.TASK_RUN_FILE, "-i", str(flow_instance_id)],
                                  stdout=outfile, stderr=subprocess.STDOUT)
            json_data = {
                "worker_process_id": pm.pid,
                "worker_hostname": socket.gethostname(),
                "flow_instance_id": flow_instance_id,
                "start_time": time.time()
            }
            redisdb.add_running_instance(flow_instance_id, json_data)
            redisdb.close()
    except:
        logging.error('message_process err \n %s', traceback.format_exc())


def main():
    logging.info("taskflow receiver is running")
    # get redis data
    redisdb = RedisDB()
    while True:
        data = redisdb.pop_msg_queue()
        if data is not None:
            message_process(int(data))
        time.sleep(1)


if __name__ == '__main__':
    main()
