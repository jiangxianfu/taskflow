# -*- coding: utf-8 -*-
"""
author: jiangxf
date: 2020-01-29
description: 该方法主要是用于单独运行模块的测试功能

"""

import logging
import unittest
from tests.test_workflow_spec import *

# from tests.test_docker import *
# from tests.test_scheduler import *
# from tests.test_taskflowdb import *
# from tests.test_task_run import *
# from tests.test_redisdb import *

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    unittest.main()
