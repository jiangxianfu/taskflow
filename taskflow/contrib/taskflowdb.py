# -*- coding: utf-8 -*-

"""
author: jiangxf
date: 2020-01-29
description: 操作数据的DB
"""

from . import settings
import pymysql
import json


class TaskFlowDB:
    """
        操作数据库类
    """

    def __init__(self):
        host = settings.MYSQL_HOST
        port = settings.MYSQL_PORT
        user = settings.MYSQL_USER
        password = settings.MYSQL_PWD
        database = settings.MYSQL_DB
        self.conn = pymysql.connect(host=host, port=port, user=user, password=password,
                                    database=database, ssl=None,
                                    autocommit=True, cursorclass=pymysql.cursors.DictCursor)

    def __del__(self):
        self.close()

    def close(self):
        try:
            if self.conn:
                self.conn.close()
        finally:
            self.conn = None

    def get_undo_taskforms(self, limit=50):
        """
        获取待运行的任务
        """
        sql = """select id,task_type,task_name,args_json 
                    from task_form where status = 'standby' and plan_runtime <= now() limit %s""" % limit
        with self.conn.cursor() as cur:
            cur.execute(sql)
            data = cur.fetchall()
            return data

    def create_instance(self, source_id, source_type, parent_id, task_type, task_name, args_json, status):
        sql = """insert into task_instance(source_id,source_type,parent_id,task_type,task_name,args_json,status)
                    values(%s,%s,%s,%s,%s,%s,%s)"""
        with self.conn.cursor() as cur:
            cur.execute(sql, (source_id, source_type, parent_id, task_type, task_name, args_json, status))
            return cur.lastrowid

    def save_taskform_status(self, form_id, status):
        sql = "update task_form set status=%s where id=%s"
        with self.conn.cursor() as cur:
            cur.execute(sql, (status, form_id))

    def get_sched_cron(self, limit=50):
        sql = """select id,cron_sched,task_type,task_name,args_python_code 
                    from task_schedule where cron_enabled=1 and status<>'running' 
                    and (trigger_next_time is null or trigger_next_time <=now()) limit %s""" % limit
        with self.conn.cursor() as cur:
            cur.execute(sql)
            data = cur.fetchall()
            return data

    def update_sched(self, action, sched_id, status, trigger_last_time=None, trigger_next_time=None):
        with self.conn.cursor() as cur:
            if action == "start":
                sql = """update tasks_schedule set trigger_last_time=%s,trigger_next_time=%s,
                                    status=%s where id=%s"""
                cur.execute(1, sql, (trigger_last_time, trigger_next_time, status, sched_id))
            elif action == "end":
                sql = """update tasks_schedule set status=%s where id=%s"""
                cur.execute(1, sql, (status, sched_id))

    def save_instance_status(self, instance_id, status, worker_hostname=None, worker_pid=None,
                             result_message=None, result_json=None):
        """
        保存实例信息状态
        """
        sql = "update task_instance set status=%s"
        lst_params = [status]
        if worker_hostname:
            sql = sql + ",worker_hostname=%s"
            lst_params.append(worker_hostname)
        if worker_pid:
            sql = sql + ",worker_pid=%s"
            lst_params.append(worker_pid)
        if result_message:
            sql = sql + ",result_message=%s"
            lst_params.append(result_message)
        if result_json:
            sql = sql + ",result_json=%s"
            lst_params.append(result_json)
        sql = sql + " where id =%s"
        lst_params.append(instance_id)
        with self.conn.cursor() as cur:
            cur.execute(sql, lst_params)

    def get_instance(self, instance_id):
        sql = "select * from task_instance where id=%s"
        with self.conn.cursor() as cur:
            cur.execute(sql, (id,))
            data = cur.fetchall()
            if data:
                return data[0]
            return None


"""
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

    def add_instance_step(self, flow_instance_id, step_num, step_name, json_kwargs, worker_name, status, message):
        sql = "insert into instance_steps(instanceid,stepnum,stepname,arguments,workername,status,message) values(%s,%s,%s,%s,%s,%s,%s)"
        return self.db.insert(sql, (flow_instance_id, step_num, step_name, json_kwargs, worker_name, status, message))

    def save_instance_step_status(self, instance_step_id, status, message):
        sql = "update instance_steps set status=%s , message=%s where id =%s"
        return self.db.execute(sql, (status, message, instance_step_id))

    def set_instance_run_data(self, flow_instance_id, keytype, keyname, keyvalue):
        sql = "insert into instance_rundata(instanceid,keyname,keyvalue,keytype) values(%s,%s,%s,%s) ON DUPLICATE KEY UPDATE keytype=%s , keyvalue=%s"
        return self.db.execute(sql, (flow_instance_id, keyname, keyvalue, keytype, keytype, keyvalue))
"""
