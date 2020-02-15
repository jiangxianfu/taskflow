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

def message_process(flow_instance_id):
    try:
        redisdb = RedisDB()
        # 获取需要运行的模块
        output_filename = settings.TASK_RUN_LOG_FORMAT % flow_instance_id
        with open(output_filename, "a") as outfile:
            pm = subprocess.Popen([settings.PYTHONBIN, "-u", settings.TASK_RUN_FILE, "-i", flow_instance_id],
                                  stdout=outfile, stderr=subprocess.STDOUT)
            json_data = {
                "worker_process_id": pm.pid,
                "worker_hostname": socket.gethostname(),
                "flow_instance_id": flow_instance_id,
                "start_time": time.time()
            }
            redisdb.add_running_instance(flow_instance_id, json_data)

    except Exception as ex:
        print(ex)


def main():
    # get redis data
    redisdb = RedisDB()
    while True:
        data = redisdb.pop_msg_queue()
        if data is not None and type(data) == int:
            message_process(data)
        time.sleep(1)


if __name__ == '__main__':
    main()
