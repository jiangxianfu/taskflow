# -*- coding: utf-8 -*-
"""
 存储一些基础的配置信息
"""
import os

# settings filename
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Redis 配置
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 1

# MySql 配置
MYSQL_HOST = ""
MYSQL_PORT = 3306
MYSQL_USER = ""
MYSQL_PWD = ""

TASK_RUN_FILE = os.path.join(BASE_DIR, 'task_run.py')
TASK_RUN_LOG_FORMAT = "/var/log/taskflow/task_run_%s.log"

#PYTHONBIN = "/usr/bin/python3"
PYTHONBIN = "python3"