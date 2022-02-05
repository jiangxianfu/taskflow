# -*- coding: utf-8 -*-
import os
import yaml
from .settings import BASE_DIR

"""
Workflow Model
===============
attribute    required   description
------------------------------------------
description  no         描述
begin        yes        用于开始的task名称
end          yes        用于接受的名称
tasks        yes        A dictionary of tasks that defines the intent of this workflow.
#######################################################################################
Task Model
===========
attribute    required   description
--------------------------------------------
module       yes        具体执行的模块名称(action_xxx,check_xxx)
on-success   yes        执行成功后要执行的action
on-failure   no         执行失败后要执行的action
retry        no         如果失败后可以重试次数
delay        no         延迟执行秒数
"""


class WorkflowSpec(object):
    """
    Workflow 规则类
    """
    _meta_schema = {
        "description": {"type": "string", "required": False, "description": "workflow description"},
        "begin": {"type": "string", "required": True, "description": "workflow start task name"},
        "end": {"type": "string", "required": True, "description": "workflow end task name"},
        "tasks": {"type": "array", "required": True, "description": "workflow tasks"}
    }

    def __init__(self, name):
        self.name = name
        self.filename = os.path.join(BASE_DIR, "workflows", "%s.yaml" % name)
        with open(self.filename, 'r', encoding='utf8') as f:
            self._spec = yaml.safe_load(f)  # type: dict
        if not isinstance(self._spec, dict) and not self._spec:
            raise ValueError("load workflow error")

    def get_meta_schema(self):
        return self._meta_schema

    def __getattr__(self, name):
        # 获取当前规则属性
        if name in self._meta_schema:
            return self._spec.get(name)
        # 获取系统属性
        return self.__getattribute__(name)
