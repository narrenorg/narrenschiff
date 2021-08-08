# Copyright 2021 Petar Nikolovski

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
