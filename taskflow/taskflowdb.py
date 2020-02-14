# -*- coding: utf-8 -*-

"""
author: jiangxf
date: 2020-01-29
description: 操作数据的DB
"""

from com.dbconfig import connect_short
from com.dbhelper import DBHelper


class TaskFlowDB(object):
    """
        操作数据库类
    """

    def __init__(self):
        self.db = DBHelper(connect_short("testdb"))

    def __del__(self):
        if self.db:
            self.db.close()
            self.db = None

    def get_undo_instances(self):
        """
        获取待处理的实例信息
        :return:
        """
        sql = "select id from instances where nexruntime <= now() and status = 'standby' limit 50;"
        data = self.db.querydic(sql)
        return data

    def save_instance_status(self, instanceid, status):
        """
        保存实例信息状态
        :param instanceid:
        :param status:
        :return:
        """
        sql = "update instances set status=%s where id =%s"
        ret = self.db.execute(sql, (status, instanceid))
        return ret

    def get_instance(self, instance_id):
        sql = "select * from instances where id =%s"
        data = self.db.querydic(sql, (instance_id,))
        if len(data) > 0:
            return data[0]
        return None

    def get_flow_step(self, flow_id, step_num):
        sql = "select * from flow_steps where flow_id=%s and step_num=%s limit 1"
        data = self.db.querydic(sql, (flow_id, step_num))
        if len(data) > 0:
            return data[0]
        return None
