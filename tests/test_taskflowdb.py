# -*- coding: utf-8 -*-
import unittest
from contrib.taskflowdb import TaskFlowDB


class TestTaskFlowDB(unittest.TestCase):
    def setUp(self):
        self.db = TaskFlowDB()

    def test_dbhelper(self):
        with self.db.conn.cursor() as cur:
            cur.execute("select 'hello' as n")
            version = cur.fetchall()
        print('ssssssssssssss', version[0]['n'])
        assert 'hello' == version[0]['n']

    def test_tables(self):
        with self.db.conn.cursor() as cur:
            cur.execute("show tables")
            data = cur.fetchall()
            assert len(data) > 0

    def test_taskflowdb(self):
        data = self.db.get_undo_taskforms()
        assert type(data) is tuple
