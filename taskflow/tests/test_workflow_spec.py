import unittest

from contrib.workflow_spec import WorkflowSpec


class TestWorkflowSpec(unittest.TestCase):

    def test_read_yaml(self):
        wf = WorkflowSpec("test_with_pause")
        print(dir(wf))
        print(wf.tasks)
        print(wf.description)
        print(wf.tasks)
        print(wf.filename)
        for t, v in wf.tasks.items():
            print(t)
            print(v)
            print(v.get("on-success"))
