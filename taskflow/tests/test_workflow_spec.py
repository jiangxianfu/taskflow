import unittest

from contrib.workflow_spec import WorkflowSpec
from contrib.workflow_context import WorkflowContext


class TestWorkflowSpec(unittest.TestCase):

    def no_test_read_yaml(self):
        wf = WorkflowSpec("test_simple")
        print(dir(wf))
        print(wf.description)
        print(wf.steps)
        print(wf.filename)
        for t, v in wf.steps.items():
            print(t)
            print(v)
            print(v.get("on-success"))

    def test_eval(self):
        wf = WorkflowSpec("test_simple")
        print("===========================")
        context = WorkflowContext(None, 1)
        for name, step in wf.steps.items():
            print("step_name:", name)
            parameters = step.get("parameters")
            for param_name, param_value in parameters.items():
                if param_value.startswith("$"):
                    if param_value.startswith("$$"):
                        param_value = param_value[1:]
                    else:
                        param_value = eval(param_value[1:], {"this": wf, "ctx": context})
                print("#", param_name, type(param_value), param_value)
