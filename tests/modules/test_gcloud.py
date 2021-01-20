import unittest

from narrenschiff.modules.gcloud import Gcloud


class GcloudTestCase(unittest.TestCase):

    def test_dry_run_supported(self):
        self.assertFalse(Gcloud({}).dry_run_supported('gcloud version'))

    def test_cmd(self):
        gcloud = Gcloud({'command': 'version'})
        expected = 'gcloud version'
        self.assertEqual(gcloud.cmd, expected)

    def test_cmd_with_args(self):
        gcloud = Gcloud({
            'command': 'container clusters create test-cluster',
            'args': {'num-nodes': '3'}
        })
        expected = "gcloud container clusters create test-cluster --num-nodes '3'"  # noqa
        self.assertEqual(gcloud.cmd, expected)
