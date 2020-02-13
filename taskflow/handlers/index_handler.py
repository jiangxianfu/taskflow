# -*- coding: utf-8 -*-
"""
author: jiangxf
date: 2020-01-29
description: 该方法主要是用于启动整个工作流程序

"""
import json

from tornado.web import RequestHandler


class IndexHandler(RequestHandler):
    def get(self):
        res = {"success": True, "message": "ok", "data": None}
        self.write(json.dumps(res))
        self.flush()

    def post(self):
        json_data = {}
        if self.request.body:
            json_data = json.loads(self.request.body)
        res = {"success": True, "message": "ok", "data": json_data}
        self.write(json.dumps(res))
        self.flush()

