# -*- coding: utf-8 -*-
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# REDIS_HOST = "127.0.0.1"
REDIS_HOST = "task-redis"
REDIS_PORT = 6379
REDIS_DB = 0

# MYSQL_HOST = "127.0.0.1"
REDIS_HOST = "task-db"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PWD = "123456"
MYSQL_DB = "taskflowdb"

PYTHONBIN = "/usr/bin/python3"

TASK_RUN_LOG_FORMAT = "/var/log/taskflow/instance_%s.log"
