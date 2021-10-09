# Copyright 2021 The Narrenschiff Authors

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
from click.testing import CliRunner
from narrenschiff.env import Env
from narrenschiff.narrenschiff import narrenschiff


class CustomModuleTestCase(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()
        self.NARRENSCHIFF_PATH = Env.NARRENSCHIFF_PATH
        Env.NARRENSCHIFF_PATH = './tests/fixtures/custom/modules'

    def test_custom_module_executed(self):
        result = self.runner.invoke(
            narrenschiff,
            ['sail', '--set-course', './tests/fixtures/custom/course.yaml']
        )
        self.assertEqual(result.exit_code, 0)

    def test_custom_module_returns_correct_value(self):
        result = self.runner.invoke(
            narrenschiff,
            ['sail', '--set-course', './tests/fixtures/custom/course.yaml']
        )
        self.assertTrue(result.output.endswith('Ahoy, Matey!\n\n'))

    def test_fail_to_load_custom_module_env_set(self):
        result = self.runner.invoke(
            narrenschiff,
            ['sail', '--set-course', './tests/fixtures/custom/halt.yaml']
        )
        self.assertEqual(result.output, 'No module "fail_to_load" found\n')

    def test_fail_to_load_custom_module_no_env_set(self):
        Env.NARRENSCHIFF_PATH = ''
        result = self.runner.invoke(
            narrenschiff,
            ['sail', '--set-course', './tests/fixtures/custom/halt.yaml']
        )
        self.assertEqual(result.output, 'No module "fail_to_load" found\n')

    def tearDown(self):
        Env.NARRENSCHIFF_PATH = self.NARRENSCHIFF_PATH
        self.runner = None
