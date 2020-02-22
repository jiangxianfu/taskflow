# -*- coding: utf-8 -*-
"""
author: jiangxf
date: 2020-01-29
description: 该方法主要是用于启动整个工作流程序

"""

import time
import logging
from redisdb import RedisDB
from taskflowdb import TaskFlowDB
import sys
import traceback

logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    logging.info("taskflow sender is running")
    taskflowdb = TaskFlowDB()
    redisdb = RedisDB()
    while True:
        data = taskflowdb.get_undo_instances()
        if len(data) == 0:
            time.sleep(30)
            continue
        sended_ids = []
        try:
            for item in data:
                redisdb.push_msg_queue(item["id"])
                sended_ids.append(item["id"])
        except:
            logging.warning("push redis err \n %s", traceback.format_exc())
        if len(sended_ids):
            for item in sended_ids:
                taskflowdb.save_instance_status(item, 'running')

        if len(sended_ids) != len(data):
            logging.error("redis data error: sended len not equal data len")
            raise Exception("redis data error")
        time.sleep(2)


if __name__ == '__main__':
    main()
