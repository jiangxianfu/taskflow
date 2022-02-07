# -*- coding: utf-8 -*-
from tornado.web import RequestHandler
import json


class IndexHandler(RequestHandler):
    def get(self):
        self.write("ok")
        self.flush()


class HealthHandler(RequestHandler):
    def get(self):
        res = {"success": True, "message": "ok", "data": ""}
        self.write(json.dumps(res))
        self.flush()
