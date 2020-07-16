import os
import unittest

from narrenschiff.chest import Chest
from narrenschiff.chest import AES256Cipher


class MockKeychain:

    key = 'key'
    spice = 'sugar'


class AES256CipherTestCase(unittest.TestCase):

    def setUp(self):
        self.aes256 = AES256Cipher(MockKeychain())

    def test_encrypt(self):
        self.assertNotEqual('value', self.aes256.encrypt('value'))

    def test_decrypt(self):
        self.assertEqual(
            'value',
            self.aes256.decrypt(self.aes256.encrypt('value'))
        )


class ChestTestCase(unittest.TestCase):

    def setUp(self):
        self.path = 'tests/fixtures/chest.yaml'
        with open(self.path, 'w') as f:
            f.write('')

        self.chest = Chest(MockKeychain(), self.path)

    def test_load_chest_file(self):
        self.assertEqual({}, self.chest.load_chest_file())

    def test_update_chest_file(self):
        before = self.chest.load_chest_file()
        self.chest.update('x', 'marks the spot')
        after = self.chest.load_chest_file()
        self.assertNotEqual(before, after)

    def test_show_variable(self):
        self.chest.update('x', 'marks the spot')
        self.assertEqual('marks the spot', self.chest.show('x'))

    def tearDown(self):
        self.chest = None
        os.remove(self.path)
