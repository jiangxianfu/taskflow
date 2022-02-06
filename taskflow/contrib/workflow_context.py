# -*- coding: utf-8 -*-
from .taskflowdb import TaskFlowDB


class WorkflowContext(object):
    def __init__(self, db: TaskFlowDB, instance_id: int):
        self.instance_id = instance_id
        self.taskflowdb = db

    def get_root_argument(self):
        return {}

    def get_step_result(self, step_name):
        return {}

    def get_step_argument(self, step_name):
        return {}
