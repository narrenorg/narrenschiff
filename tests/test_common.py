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

import os
import uuid
import unittest

from narrenschiff.common import is_yaml
from narrenschiff.common import is_jinja
from narrenschiff.common import flatten
from narrenschiff.common import DeleteFile
from narrenschiff.common import get_chest_file_path
from narrenschiff.common import AmbiguousConfiguration


class CommonFunctionsTestCase(unittest.TestCase):

    def test_is_yaml(self):
        self.assertTrue(is_yaml('file.yaml'))
        self.assertTrue(is_yaml('file.yml'))

    def test_is_yaml_fail(self):
        self.assertFalse(is_yaml('file.toml'))

    def test_is_jinja(self):
        self.assertTrue(is_jinja('file.j2'))
        self.assertTrue(is_jinja('file.jinja2'))

    def test_is_jinja_fail(self):
        self.assertFalse(is_jinja('file.jin'))
        self.assertFalse(is_jinja('file.jinja'))

    def test_flatten_list(self):
        input_list = ['a', ['b', 'c']]
        output_list = ['a', 'b', 'c']
        self.assertEqual(output_list, flatten(input_list))

    def test_get_chest_file_path(self):
        location = 'tests/fixtures/chest_test'
        path = get_chest_file_path(location)
        chest_file = os.path.join(os.getcwd(), location, 'chest.yaml')
        self.assertEqual(chest_file, path)

    def test_chest_file_does_not_exists(self):
        with self.assertRaises(AmbiguousConfiguration):
            get_chest_file_path('tests/fixtures/not_a_chest')

    def test_duplicate_chest_files(self):
        with self.assertRaises(AmbiguousConfiguration):
            get_chest_file_path('tests/fixtures/duplicate_chest')


class DeleteFileTestCase(unittest.TestCase):

    def setUp(self):
        self.path = os.path.join('/tmp', f'{uuid.uuid4()}.test')
        with open(self.path, 'w'):
            pass
        self.test_file = DeleteFile(self.path)

    def test_delete_file(self):
        self.assertTrue(os.path.exists(self.path))
        self.test_file.delete()
        self.assertFalse(os.path.exists(self.path))
