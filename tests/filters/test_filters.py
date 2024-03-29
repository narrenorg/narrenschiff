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

from narrenschiff.filters import filters


class FiltersTestCase(unittest.TestCase):

    def test_base64(self):
        self.assertEqual('dGVzdA==', filters['b64enc']('test'))

    def test_rtrim(self):
        self.assertEqual('value', filters['rtrim']('value     '))

    def test_secretmap(self):
        self.assertEqual('{{secretmap}}/test', filters['secretmap']('test'))
