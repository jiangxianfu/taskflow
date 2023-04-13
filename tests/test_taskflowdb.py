# -*- coding: utf-8 -*-
import unittest
from core.taskflowdb import TaskFlowDB


class TestTaskFlowDB(unittest.TestCase):
    def setUp(self):
        self.db = TaskFlowDB()

    def test_dbhelper(self):
        with self.db.conn.cursor() as cur:
            cur.execute("select 'hello' as n")
            version = cur.fetchall()
        print('dbhelper hello:', version[0]['n'])
        self.assertEqual('hello',version[0]['n'])

    def test_tables(self):
        with self.db.conn.cursor() as cur:
            cur.execute("show tables")
            data = cur.fetchall()
            print("db tables",data)
            self.assertTrue(data)

    def test_taskflowdb(self):
        data = self.db.get_undo_taskforms()
        self.assertIsInstance(data,tuple)
