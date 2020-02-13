# -*- coding:utf-8 -*-
from datetime import datetime
import time


def ping():
    """
    test ping
    :return: None
    """
    for i in range(3):
        print(i, "ok", datetime.now())
        time.sleep(1)
