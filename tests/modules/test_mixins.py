import unittest

from narrenschiff.modules.mixins import KubectlDryRunMixin


class KubectlDryRunMixinTestCase(unittest.TestCase):

    def setUp(self):
        self.mixin = KubectlDryRunMixin()

    def test_proprty_exists(self):
        self.assertEqual(self.mixin.dry_run, '--dry-run=server')

    def test_dry_run_supported(self):
        self.assertTrue(
            self.mixin.dry_run_supported('kubectl apply -f /nonexistent')
        )

    def test_dry_run_not_supported(self):
        self.assertFalse(
            self.mixin.dry_run_supported('kubectl nonexistent')
        )
