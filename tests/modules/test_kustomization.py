import unittest

from narrenschiff.templating import Template
from narrenschiff.modules.kustomization import Kustomization
from narrenschiff.modules.common import NarrenschiffModuleException


class KustomizationTestCase(unittest.TestCase):

    def test_cmd_pass(self):
        command = 'examples/nonexistent/'
        template = Template()
        template.tmp = '/tmp/narrenschiff-test'

        kustomization = Kustomization(command)
        self.assertEqual(
            kustomization.cmd,
            f'kubectl apply -k "{template.tmp}/{command}"'
        )

    def test_cmd_exception(self):
        with self.assertRaises(NarrenschiffModuleException):
            Kustomization({'command': 'arg'}).cmd
