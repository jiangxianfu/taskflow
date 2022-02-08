# -*- coding: utf-8 -*-

import unittest

from contrib.workflow_spec import WorkflowSpec
from contrib.workflow_context import WorkflowContext
from contrib.taskflowdb import TaskFlowDB


class TestWorkflowSpec(unittest.TestCase):

    def no_test_read_yaml(self):
        wf = WorkflowSpec("test_simple")
        print('check workflow dir',dir(wf))
        print('test workflow description:',wf.description)
        print('test workflow steps:',wf.steps)
        print('test workflow filename:',wf.filename)
        for t, v in wf.steps.items():
            print("step:",t)
            print("step object:",v)
            print("step-on-success:",v.get("on-success"))
            print("step-on-success-eval:",wf.get_expr_value(v.get("on-success")))

    def test_eval(self):
        wf = WorkflowSpec("test_simple")
        print("===========================")
        taskflowdb = TaskFlowDB()
        context = WorkflowContext(taskflowdb, 1, 0)
        for name, step in wf.steps.items():
            print("step_name:", name)
            parameters = step.get("parameters")
            for param_name, param_value in parameters.items():
                if param_value.startswith("$"):
                    if param_value.startswith("$$"):
                        param_value = param_value[1:]
                    else:
                        param_value = eval(param_value[1:], {"this": wf, "ctx": context})
                print("test_eval:", param_name, type(param_value), param_value)
