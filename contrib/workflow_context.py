# -*- coding: utf-8 -*-
from .taskflowdb import TaskFlowDB
import json

class WorkflowContext(object):
    def __init__(self, db: TaskFlowDB, instance_id: int, parent_id: int):
        self.instance_id = instance_id
        self.parent_id = parent_id
        self.taskflowdb = db

    def get_root_argument(self):
        if self.parent_id >0:
            data = self.taskflowdb.get_instance_json(True,instance_id=self.parent_id)
        else:
            data = self.taskflowdb.get_instance_json(True,instance_id=self.instance_id)
        if data:
            data = json.loads(data)
            return data       
        return {}
    def get_step_argument(self, step_name):
        if self.parent_id >0:
            data = self.taskflowdb.get_instance_json(True,parent_id=self.parent_id,name=step_name)
        else:
            data = self.taskflowdb.get_instance_json(True,instance_id=self.instance_id,name=step_name)
        if data:
            data = json.loads(data)
            return data
        return {}
    def get_step_result(self, step_name):
        if self.parent_id >0:
            data = self.taskflowdb.get_instance_json(False,parent_id=self.parent_id,name=step_name)
        else:
            data = self.taskflowdb.get_instance_json(False,instance_id=self.instance_id,name=step_name)
        if data:
            data = json.loads(data)
            return data
        return {}

    
