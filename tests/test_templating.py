import logging
import unittest
from unittest import mock

from tests.mocks import MockKeychain

from narrenschiff.templating import PlainVars
from narrenschiff.templating import ChestVars
from narrenschiff.templating import SecretmapVars
from narrenschiff.templating import Template


logging.disable(logging.CRITICAL)


class PlainVarsTestCase(unittest.TestCase):

    def setUp(self):
        self.vars = PlainVars('tests/fixtures/vars/')

    def test_load_vars(self):
        vars = self.vars.load_vars()
        self.assertEqual([{'y': 1}, {'x': 1}], vars)

    def tearDown(self):
        self.vars = None


class ChestVarsTestCase(unittest.TestCase):

    def setUp(self):
        self.vars = ChestVars('tests/fixtures/vars/')

    @mock.patch(
        'narrenschiff.templating.Keychain',
        mock.MagicMock(return_value=MockKeychain)
    )
    def test_load_vars(self):
        vars = self.vars.load_vars()
        self.assertEqual([{'mistery': 'Password123!'}], vars)

    def tearDown(self):
        self.vars = None


class SecretmapVarsTestCase(unittest.TestCase):

    def setUp(self):
        self.vars = SecretmapVars('tests/fixtures/vars/')

    def test_load_vars(self):
        vars = self.vars.load_vars()
        self.assertEqual([{'dev_values': 'values.yaml'}], vars)

    def tearDown(self):
        self.vars = None


class TemplateTestCase(unittest.TestCase):

    def setUp(self):
        self.template = Template()

    def test_find_duplicates(self):
        duplicates = self.template.find_duplicates(['namespace', 'secret'])
        self.assertFalse(duplicates)

    def test_find_duplicates_fail(self):
        duplicates = self.template.find_duplicates(['namespace', 'namespace'])
        self.assertTrue(duplicates)

    def tearDown(self):
        self.template = None
