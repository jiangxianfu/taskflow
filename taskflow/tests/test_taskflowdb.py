# -*- coding: utf-8 -*-

import settings
from com.dbconfig import connect_mysql
from com.dbhelper import DBHelper
from taskflowdb import TaskFlowDB

print(settings.MYSQL_USER)
conn = connect_mysql(settings.MYSQL_HOST, settings.MYSQL_PORT,
                     settings.MYSQL_USER, settings.MYSQL_PWD,
                     settings.MYSQL_DB)
db = DBHelper(conn)


def test_dbhelper():
    version = db.querydic("select 'hello'")
    assert 'hello' in version[0]


def test_tables():
    assert len(db.querydic("show tables")) > 0


def test_taskflowdb():
    flowdb = TaskFlowDB()
    data = flowdb.get_undo_instances()
    assert type(data) is list


