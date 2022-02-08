# -*- coding: utf-8 -*-
"""
author: jiangxf
date: 2020-01-29
description: 该方法主要是用于启动整个工作流程序


# 获取待运行的任务
# 创建任务
# 发送到消息队列
# 分配任务到消息队列中

"""

import time
import logging
from contrib.redisdb import RedisDB
import sys

logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    logging.info("taskflow checker is running")
    redisdb = RedisDB()
    while True:
        data = redisdb.fetch_check_queue()
        if data:
            for instance_id, score in data:
                redisdb.push_run_queue(instance_id)
                redisdb.remove_check_queue(instance_id)
                time.sleep(3)
        else:
            time.sleep(300)


if __name__ == '__main__':
    main()
