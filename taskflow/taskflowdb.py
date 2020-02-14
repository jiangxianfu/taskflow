# -*- coding: utf-8 -*-

"""
author: jiangxf
date: 2020-01-29
description: 操作数据的DB
"""

from com.dbconfig import connect_short
from com.dbhelper import DBHelper
import json


class TaskFlowDB:
    """
        操作数据库类
    """

    def __init__(self):
        self.db = DBHelper(connect_short("testdb"))

    def __del__(self):
        self.close()

    def close(self):
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

    def save_instance_status(self, instance_id, status, cur_step_num=None, cur_step_runcount=None, next_runtime=None):
        """
        保存实例信息状态
        """
        sql = "update instances set status=%s"
        lst_params = [status]
        if cur_step_num:
            sql = sql + ",curstepnum=%s"
            lst_params.append(cur_step_num)
        if cur_step_runcount:
            sql = sql + ",curstepruncount=%s"
            lst_params.append(cur_step_runcount)
        if next_runtime:
            sql = sql + ",nextruntime=%s"
            lst_params.append(next_runtime)
        sql = sql + " where id =%s"
        lst_params.append(instance_id)
        ret = self.db.execute(sql, lst_params)
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

    def get_module(self, module_name):
        sql = "select * from modules where module_name=%s limit 1"
        data = self.db.querydic(sql, (module_name,))
        if len(data) > 0:
            return data[0]
        return None

    def get_instance_run_data(self, instance_id):
        sql = "select keyname,keyvalue,keytype from instance_rundata where instanceid=%s"
        data = self.db.querydic(sql, (instance_id,))
        dict_data = {}
        for item in data:
            if item["keytype"] == "object":
                dict_data[item["keyname"]] = json.loads(item["keyvalue"])
            else:
                dict_data[item["keyname"]] = item["keyvalue"]
        return dict_data

    def add_instance_step(self, flow_instance_id, step_num, step_name, json_kwargs, status, message):
        sql = "insert into instance_steps(instanceid,stepnum,stepname,arguments,status,message) values(%s,%s,%s,%s,%s,%s)"
        return self.db.insert(sql, (flow_instance_id, step_num, step_name, json_kwargs, status, message))

    def save_instance_step_status(self, instance_step_id, status, message):
        sql = "update instance_steps set status=%s , message=%s where id =%s"
        return self.db.execute(sql, (status, message, instance_step_id))

    def set_instance_run_data(self, flow_instance_id, keytype, keyname, keyvalue):
        sql = "insert into instance_rundata(instanceid,keyname,keyvalue,keytype) values(%s,%s,%s,%s) ON DUPLICATE KEY UPDATE keytype=%s , keyvalue=%s"
        return self.db.execute(sql, (flow_instance_id, keyname, keyvalue, keytype, keytype, keyvalue))
