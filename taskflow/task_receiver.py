# -*- coding: utf-8 -*-
"""
author: jiangxf
date: 2020-01-29
description: 该方法主要是用于启动整个工作流程序

"""

import traceback
import time
import os
import subprocess
import redis
import settings


base_dir = os.path.dirname(os.path.abspath(__file__))

def message_process(flow_instance_id):
    try:
        # get instance id
        # 获取需要运行的模块
        filename = os.path.join(base_dir, 'task_run.py')
        output_filename = "/var/log/taskflows/task_run_%s.log" % flow_instance_id
        with open(output_filename, "a") as outfile:
            subprocess.Popen(["python3", "-u", filename, "-i", flow_instance_id], stdout=outfile, stderr=subprocess.STDOUT)
        #save subprocessid,flow_instance_id,worker_host_name to redis
    except Exception as ex:
        print(ex)


def main():
    # get redis data
    try:
        conn = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
        while True:
            data = conn.rpop("taskflow:messagequeues")
            if data is not None and type(data) == int:
                message_process(data)
            time.sleep(1)
    except:
        print(traceback.format_exc())
        time.sleep(3)

if __name__ == '__main__':
    main()
