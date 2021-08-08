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
import io
import sys
import yaml
import filecmp
import unittest

from tests.mocks import MockKeychain

from narrenschiff.secretmap import Secretmap


class SecretmapTestCase(unittest.TestCase):

    def setUp(self):
        self.path = 'tests/fixtures/secretmap/'
        self.source = os.path.join(self.path, 'dev.yaml')
        self.secretmap = Secretmap(MockKeychain(), self.path)

    def test_upsert(self):
        self.secretmap.upsert(src=self.source,
                              dest='encrypted.yaml',
                              treasure='dev')
        with open(os.path.join(self.path, 'secretmap.yaml'), 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)

        self.assertEqual(config['dev'], 'encrypted.yaml')

    @unittest.skip('See CHANGELOG for v2.0.0 and v2.0.1')
    def test_decrypt(self):
        self.secretmap.upsert(src=self.source,
                              dest='encrypted.yaml',
                              treasure='dev')
        self.secretmap.decrypt(dest=os.path.join(self.path, 'decrypted.yaml'),
                               treasure='dev')

        compare = filecmp.cmp(
            os.path.join(self.path, 'decrypted.yaml'),
            os.path.join(self.path, 'dev.yaml')
        )

        self.assertTrue(compare)

    def test_peek(self):
        self.secretmap.upsert(src=self.source,
                              dest='encrypted.yaml',
                              treasure='dev')

        with open(os.path.join(self.path, 'dev.yaml'), 'r') as f:
            expected = f.read()

        # I need this to capture STDOUT so I can check the output
        stdout = sys.stdout = io.StringIO()
        self.secretmap.peek(treasure='dev')
        sys.stdout = sys.__stdout__
        self.assertEqual(stdout.getvalue(), expected)

    def test_find(self):
        self.secretmap.upsert(src=self.source,
                              dest='encrypted.yaml',
                              treasure='dev')

        stdout = sys.stdout = io.StringIO()
        self.secretmap.find('ClusterIP', 'dev')
        sys.stdout = sys.__stdout__
        self.assertEqual(
            # re.sub(r'\x1b\[\d+m', '', stdout.getvalue(), flags=re.MULTILINE)
            stdout.getvalue(),
            # 'dev:15:  type: ClusterIP\n'
            '\033[35mdev\033[0m:\033[32m15\033[0m:  type: \033[31mClusterIP\033[0m\n'  # noqa
        )

    def test_diff(self):
        expected = '--- dev\n+++ prod\n@@ -13,7 +13,7 @@\n \n service:\n   type: ClusterIP\n-  port: 5000\n+  port: 4000\n \n resources: {}\n   # We usually recommend not to specify default resources and to leave this as a conscious\n'  # noqa

        dev = os.path.join(self.path, 'dev.yaml')
        prod = os.path.join(self.path, 'prod.yaml')

        self.secretmap.upsert(src=dev,
                              dest='encrypted-dev.yaml',
                              treasure='dev')
        self.secretmap.upsert(src=prod,
                              dest='encrypted-prod.yaml',
                              treasure='prod')

        stdout = sys.stdout = io.StringIO()
        self.secretmap.diff(secretmaps=('dev', 'prod'))
        sys.stdout = sys.__stdout__
        self.assertEqual(stdout.getvalue(), expected)

    def test_destroy(self):
        self.secretmap.upsert(src=self.source,
                              dest='encrypted.yaml',
                              treasure='dev')

        self.secretmap.destroy(treasure='dev')

        with open(os.path.join(self.path, 'secretmap.yaml'), 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)

        self.assertEqual(config.get('dev', ''), '')

    def tearDown(self):
        self.secretmap = None

        with open(os.path.join(self.path, 'secretmap.yaml'), 'w') as f:
            f.write('')

        try:
            os.remove(os.path.join(self.path, 'encrypted.yaml'))
            os.remove(os.path.join(self.path, 'encrypted-dev.yaml'))
            os.remove(os.path.join(self.path, 'encrypted-prod.yaml'))
            os.remove(os.path.join(self.path, 'decrypted.yaml'))
        except FileNotFoundError:
            pass
