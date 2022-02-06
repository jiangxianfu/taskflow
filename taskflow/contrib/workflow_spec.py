# -*- coding: utf-8 -*-
import os
import yaml
from .settings import BASE_DIR
from .utils import CustomJSONEncoder
import json

"""
Workflow Model
===============
attribute    required   description
------------------------------------------
description  no         描述
begin_step        yes        用于开始的task名称
end_step          yes        用于接受的名称
steps        yes        A dictionary of steps that defines the intent of this workflow.
#######################################################################################
Task Model
===========
attribute    required   description
--------------------------------------------
module       yes        具体执行的模块名称(action_xxx,check_xxx)
parameters   yes        模块对应的参数
on-success   yes        执行成功后要执行的step_name
on-failure   no         执行失败后要执行的step_name
retry        no         如果失败后可以重试次数
delay        no         延迟执行秒数
"""


class WorkflowSpec(object):
    """
    Workflow 规则类
    """
    _meta_schema = {
        "description": {"type": "string", "required": False, "description": "workflow description"},
        "begin_step": {"type": "string", "required": True, "description": "workflow start step name"},
        "end_step": {"type": "string", "required": True, "description": "workflow end step name"},
        "steps": {"type": "array", "required": True, "description": "workflow steps"}
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

    def get_step_parameters(self, instance_id, step_name, to_json=False):
        step_item = self.steps[step_name]
        data = {}
        if to_json:
            data = json.dumps(data, ensure_ascii=False, cls=CustomJSONEncoder)
        return {}
