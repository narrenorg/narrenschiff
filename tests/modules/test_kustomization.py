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
