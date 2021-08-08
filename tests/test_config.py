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
from unittest import mock

from narrenschiff.config import Keychain
from narrenschiff.config import KubectlContext


class MockNarrenschiffConfiguration:

    def __init__(self):
        self.key = 'key'
        self.spice = 'spice'
        self.context = {}


class KeychainTestCase(unittest.TestCase):

    @mock.patch(
        'narrenschiff.config.NarrenschiffConfiguration',
        mock.MagicMock(return_value=MockNarrenschiffConfiguration())
    )
    def test_keychain_returns_key_and_spice(self):
        keychain = Keychain()

        self.assertEqual(keychain.key, 'key')
        self.assertEqual(keychain.spice, 'spice')


@mock.patch(
    'subprocess.run',
    mock.MagicMock(
        return_value=type(
            'S',
            (),
            {'stdout': b'test_context', 'returncode': 0}
        )
    )
)
class KubectlContextTestCase(unittest.TestCase):

    @mock.patch(
        'narrenschiff.config.NarrenschiffConfiguration',
        mock.MagicMock(return_value=MockNarrenschiffConfiguration())
    )
    def test_class_returns_default_values(self):
        context = KubectlContext()

        self.assertEqual(context.name, KubectlContext.NAME)
        self.assertFalse(context.use)

    @mock.patch(
        'narrenschiff.config.NarrenschiffConfiguration',
        mock.MagicMock(
            return_value=type('C', (), {'context': {'use': 'false'}})
        )
    )
    def test_use_is_false_for_string_input(self):
        context = KubectlContext()
        self.assertFalse(context.use)

    @mock.patch(
        'narrenschiff.config.NarrenschiffConfiguration',
        mock.MagicMock(
            return_value=type('C', (), {'context': {'use': 'true'}})
        )
    )
    def test_use_is_true_for_string_input(self):
        context = KubectlContext()
        self.assertTrue(context.use)

    @mock.patch(
        'narrenschiff.config.NarrenschiffConfiguration',
        mock.MagicMock(
            return_value=type('C', (), {'context': {'use': 0}})
        )
    )
    def test_use_is_false_for_integer_input(self):
        context = KubectlContext()
        self.assertFalse(context.use)

    @mock.patch(
        'narrenschiff.config.NarrenschiffConfiguration',
        mock.MagicMock(
            return_value=type('C', (), {'context': {'use': 1}})
        )
    )
    def test_use_is_true_for_integer_input(self):
        context = KubectlContext()
        self.assertTrue(context.use)

    @mock.patch(
        'narrenschiff.config.NarrenschiffConfiguration',
        mock.MagicMock(
            return_value=type('C', (), {'context': {'use': False}})
        )
    )
    def test_use_is_false_for_boolean_input(self):
        context = KubectlContext()
        self.assertFalse(context.use)

    @mock.patch(
        'narrenschiff.config.NarrenschiffConfiguration',
        mock.MagicMock(
            return_value=type('C', (), {'context': {'use': True}})
        )
    )
    def test_use_is_true_for_boolean_input(self):
        context = KubectlContext()
        self.assertTrue(context.use)


@mock.patch(
    'narrenschiff.config.NarrenschiffConfiguration',
    mock.MagicMock(
        return_value=type('C', (), {'context': {'use': True}})
    )
)
@mock.patch(
    'subprocess.run',
    mock.MagicMock(
        return_value=type(
            'S',
            (),
            {'stderr': b'error', 'returncode': 1}
        )
    )
)
class KubectlContextNoContextFoundTestCase(unittest.TestCase):

    def test_fails_when_current_context_cannot_be_obtained(self):
        with self.assertRaises(SystemExit):
            KubectlContext()


class KubectlContextSwitchingTestCase(unittest.TestCase):

    @mock.patch(
        'subprocess.run',
        mock.MagicMock(
            return_value=type(
                'S',
                (),
                {'stdout': b'success', 'returncode': 0}
            )
        )
    )
    def test_context_switch_success(self):
        context = KubectlContext()
        context.switch_context = ('old_context', 'new_context')
        context.switch()
        self.assertEqual(
            context.switch_context, ('new_context', 'old_context')
        )

    @mock.patch(
        'subprocess.run',
        mock.MagicMock(
            return_value=type(
                'S',
                (),
                {'stderr': b'error', 'returncode': 1}
            )
        )
    )
    def test_context_switch_failed(self):
        context = KubectlContext()
        context.switch_context = ('old_context', 'new_context')
        with self.assertRaises(SystemExit):
            context.switch()
