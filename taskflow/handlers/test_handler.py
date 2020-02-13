# -*- coding: utf-8 -*-

import json

from tornado.web import RequestHandler
from com.dbconfig import connect_short
from com.dbhelper import DBHelper


class TestHandler(RequestHandler):
    def get(self):
        db = DBHelper(connect_short("testdb"))
        data = db.querydic("select id,name from mytest")
        print(data)
        res = {"success": True, "message": "ok", "data": data}
        self.write(json.dumps(res))
        self.flush()

    def post(self):
        json_data = json.loads(self.request.body)
        res = {"success": True, "message": "ok", "data": json_data}
        self.write(json.dumps(res))
        self.flush()
