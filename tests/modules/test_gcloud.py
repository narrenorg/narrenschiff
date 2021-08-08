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
        expected = ("gcloud container clusters create "
                    "test-cluster --num-nodes '3'")
        self.assertEqual(gcloud.cmd, expected)
