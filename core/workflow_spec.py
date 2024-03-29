# -*- coding: utf-8 -*-
import os
import yaml
from .settings import BASE_DIR
from .utils import CustomJSONEncoder
from .taskflowdb import TaskFlowDB
import json


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

    def __init__(self, name, db: TaskFlowDB, instance_id: int, parent_id: int):
        self.name = name
        self.filename = os.path.join(BASE_DIR, "workflows", "%s.yaml" % name)
        with open(self.filename, 'r', encoding='utf8') as f:
            self._spec = yaml.safe_load(f)  # type: dict
        if not isinstance(self._spec, dict) and not self._spec:
            raise ValueError("load workflow error")
        self.instance_id = instance_id
        self.parent_id = parent_id
        self.db = db
        self.cache = {}

    def get_meta_schema(self):
        """
        获取元数据信息
        :return: dict
        """
        return self._meta_schema

    def __getattr__(self, name):
        # 获取当前规则属性
        if name in self._meta_schema:
            return self._spec.get(name)
        # 获取系统属性
        return self.__getattribute__(name)

    def get_root_argument(self):
        """
        获取流程初始化参数信息
        :return: dict
        """
        cache_key = 'root_argument'
        if cache_key in self.cache:
            return self.cache[cache_key]
        if self.parent_id > 0:
            data = self.db.get_instance_json(True, instance_id=self.parent_id)
        else:
            data = self.db.get_instance_json(True, instance_id=self.instance_id)
        if data:
            data = json.loads(data)
            self.cache[cache_key] = data
            return data
        self.cache[cache_key] = {}
        return {}

    def get_step_argument(self, step_name):
        """
        获取步骤对应的输入值
        :param step_name: str
        :return: dict
        """
        cache_key = 'step_argument:%s' % step_name
        if cache_key in self.cache:
            return self.cache[cache_key]
        if self.parent_id > 0:
            data = self.db.get_instance_json(True, parent_id=self.parent_id, name=step_name)
        else:
            data = self.db.get_instance_json(True, instance_id=self.instance_id, name=step_name)
        if data:
            data = json.loads(data)
            self.cache[cache_key] = data
            return data
        self.cache[cache_key] = {}
        return {}

    def get_step_result(self, step_name):
        """
        获取步骤对应的输出值
        :param step_name: str
        :return: dict
        """
        cache_key = 'step_result:%s' % step_name
        if cache_key in self.cache:
            return self.cache[cache_key]
        if self.parent_id > 0:
            data = self.db.get_instance_json(False, parent_id=self.parent_id, name=step_name)
        else:
            data = self.db.get_instance_json(False, instance_id=self.instance_id, name=step_name)
        if data:
            data = json.loads(data)
            self.cache[cache_key] = data
            return data
        self.cache[cache_key] = {}
        return {}

    def get_step_parameters(self, step_name: str, to_json: bool = False):
        """
        获取步骤对应的参数值
        :param step_name: str
        :param to_json: bool
        :return: dict or str
        """
        step_item = self.steps[step_name]
        parameters = step_item.get("parameters")
        data = {}
        for param_name, param_eval in parameters.items():
            data[param_name] = self.expr_value(param_eval)
        if to_json:
            data = json.dumps(data, ensure_ascii=False, cls=CustomJSONEncoder)
        return data

    def get_step_name(self, expr):
        return self.expr_value(expr)

    def expr_value(self, expr):
        if not isinstance(expr, str):
            return expr
        arguments = {"this": self}
        # 判断当前是否是表达式
        if expr.startswith("$"):
            # 如果是转义符则转换
            # 如果是表达式则使用eval进行计算得出
            if expr.startswith("$$"):
                result = expr[1:]
            else:
                result = eval(expr[1:], arguments)
        else:
            result = expr
        return result
