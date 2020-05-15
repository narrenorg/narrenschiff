import os
import uuid
import unittest

from narrenschiff.common import is_yaml
from narrenschiff.common import flatten
from narrenschiff.common import DeleteFile
from narrenschiff.common import get_chest_file_path
from narrenschiff.common import AmbiguousConfiguration


class CommonFunctionsTestCase(unittest.TestCase):

    def test_is_yaml(self):
        self.assertEqual(True, is_yaml('file.yaml'))
        self.assertEqual(True, is_yaml('file.yml'))

    def test_is_yaml_fail(self):
        self.assertEqual(False, is_yaml('file.toml'))

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
