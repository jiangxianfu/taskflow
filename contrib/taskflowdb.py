# -*- coding: utf-8 -*-

"""
author: jiangxf
date: 2020-01-29
description: 操作数据的DB
"""

from . import settings
import pymysql
from pymysql.cursors import DictCursor


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
                                    autocommit=True, cursorclass=DictCursor)

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

    def create_instance(self, name, source_id, source_type, parent_id, task_type, task_name, args_json, status):
        sql = """insert into task_instance(name,source_id,source_type,parent_id,task_type,task_name,args_json,status)
                    values(%s,%s,%s,%s,%s,%s,%s,%s)"""
        with self.conn.cursor() as cur:
            cur.execute(sql, (name, source_id, source_type, parent_id, task_type, task_name, args_json, status))
            return cur.lastrowid

    def save_taskform_status(self, form_id, status):
        sql = "update task_form set status=%s where id=%s"
        with self.conn.cursor() as cur:
            cur.execute(sql, (status, form_id))

    def get_sched_cron(self, limit=50):
        sql = """select id,cron_sched,task_type,task_name,args_python_code 
                    from task_schedule where cron_enabled=1 and status not in ('running','pause')
                    and (trigger_next_time is null or trigger_next_time <=now()) limit %s""" % limit
        with self.conn.cursor() as cur:
            cur.execute(sql)
            data = cur.fetchall()
            return data

    def update_sched(self, action, sched_id, status, trigger_last_time=None, trigger_next_time=None):
        with self.conn.cursor() as cur:
            if action == "start":
                sql = """update task_schedule set trigger_last_time=%s,trigger_next_time=%s,
                                    status=%s where id=%s"""
                cur.execute(1, sql, (trigger_last_time, trigger_next_time, status, sched_id))
            elif action == "end":
                sql = """update task_schedule set status=%s where id=%s"""
                cur.execute(1, sql, (status, sched_id))

    def save_instance_status(self, instance_id, status, worker_hostname=None, worker_pid=None,
                             result_message=None, result_json=None,retry_count=None):
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
        if retry_count:
            sql = sql + ",retry_count=%s"
            lst_params.append(retry_count)
        sql = sql + " where id =%s"
        lst_params.append(instance_id)
        with self.conn.cursor() as cur:
            cur.execute(sql, lst_params)

    def get_instance(self, instance_id):
        sql = "select * from task_instance where id=%s"
        with self.conn.cursor() as cur:
            cur.execute(sql, (instance_id,))
            data = cur.fetchall()
            if data:
                return data[0]
            return None
    def get_instance_json(is_input,instance_id=0,parent_id=0,name=None):
        paramlist=[]
        sql = ""
        if instance_id:
            sql = sql + " and instance_id=%s"
            paramlist.append(instance_id)
        if parent_id:
            sql = sql + " and parent_id=%s"
            paramlist.append(parent_id)
        if name:
            sql = sql + " and name=%s"
            paramlist.append(name)
        if sql and paramlist:
            sql = "select %s from task_instance where %s order by id desc limit 1;" % (
                "args_json" if is_input else "result_json",sql[5:])
            with self.conn.cursor() as cur:
                cur.execute(sql,paramlist)
                data = cur.fetchall()
                if data:
                    return data[0]
        return None
        