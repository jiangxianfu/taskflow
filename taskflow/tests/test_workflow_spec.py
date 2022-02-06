import unittest

from contrib.workflow_spec import WorkflowSpec


class TestWorkflowSpec(unittest.TestCase):

    def test_read_yaml(self):
        wf = WorkflowSpec("test_with_pause")
        print(dir(wf))
        print(wf.description)
        print(wf.steps)
        print(wf.filename)
        for t, v in wf.steps.items():
            print(t)
            print(v)
            print(v.get("on-success"))
