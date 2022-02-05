# -*- coding: utf-8 -*-
"""
author: jiangxf
date: 2020-01-29
description: 该方法主要是用于启动整个工作流程序

"""

from tornado.httpserver import HTTPServer
from tornado.web import Application
from tornado.ioloop import IOLoop
from handlers.index_handler import IndexHandler, HealthHandler
import platform

application = Application(handlers=[
    (r"^/$", IndexHandler),
    (r"^/health$", HealthHandler)
])

if __name__ == '__main__':
    sys_type = str(platform.system()).lower()
    server = HTTPServer(application, xheaders=True)
    server.bind(8000)
    print(sys_type)
    if sys_type != "windows":
        print("start multiple sub processes")
        server.start(0)  # Forks multiple sub-processes
    else:
        print("start single process")
        server.start()
    print("starting...")
    IOLoop.current().start()
