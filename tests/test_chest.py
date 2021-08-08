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
import unittest

from tests.mocks import MockKeychain

from narrenschiff.chest import Chest
from narrenschiff.chest import AES256Cipher


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
