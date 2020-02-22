# -*- coding:utf-8 -*-
from datetime import datetime
import time
import json


def ping():
    """
    test ping
    :return: None
    """
    for i in range(3):
        print(i, "ok", datetime.now())
        time.sleep(1)


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)
