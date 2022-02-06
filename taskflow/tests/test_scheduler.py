# -*- coding:utf-8 -*-
import datetime
import unittest

from scheduler import get_arguments


class TestScheduler(unittest.TestCase):
    def test_python_code(self):
        code = """import datetime
import requests
import time
def get_arguments(**kwargs):
    data={}
    data["start_time"]=int((time.time()-100000)*1000)
    data["end_time"]=int(time.time()*1000)
    data["data"]='ok' #requests.get('url',timeout=60).strptime('%Y-%M-%d')
    print(kwargs.get('run_time'))
    return data
"""
        json_data = get_arguments(code, datetime.datetime.now())
        print(json_data)
