# -*- coding: utf-8 -*-

import unittest

from core.workflow_spec import WorkflowSpec
from core.taskflowdb import TaskFlowDB


class TestWorkflowSpec(unittest.TestCase):

    def setUp(self) -> None:
        self.db = TaskFlowDB()

    def test_read_yaml(self):
        wf = WorkflowSpec("test_simple", self.db, 1, 0)
        print('check workflow dir', dir(wf))
        print('test workflow description:', wf.description)
        print('test workflow steps:', wf.steps)
        print('test workflow filename:', wf.filename)
        for t, v in wf.steps.items():
            print("step:", t)
            print("step object:", v)
            print("step-on-success:", v.get("on-success"))
            print("step-on-success-eval:", wf.get_step_name(v.get("on-success")))

    def test_eval(self):
        wf = WorkflowSpec("test_simple", self.db, 1, 0)
        print("===========================")
        for name, step in wf.steps.items():
            print("step_name:", name)
            parameters = step.get("parameters")
            wf.get_step_parameters(name)
            for param_name, param_value in parameters.items():
                if param_value.startswith("$"):
                    if param_value.startswith("$$"):
                        param_value = param_value[1:]
                    else:
                        param_value = eval(param_value[1:], {"this": wf})
                print("test_eval:", param_name, type(param_value), param_value)
