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

from narrenschiff.autocomplete import ShellAutocomplete


class ShellAutocompleteTestCase(unittest.TestCase):

    def setUp(self):
        self.autocomplete = ShellAutocomplete()
        self.script = (
            '\n\n'
            '### narrenschiff-autocompletion-start ###\n'
            'eval "$(_NARRENSCHIFF_COMPLETE=source_bash narrenschiff)"\n'
            '### narrenschiff-autocompletion-end ###\n'
        )

    def test_autocompletion_script(self):
        self.assertEqual(
            self.autocomplete.autocompletion_script(), self.script
        )

    def test_autocompletion_enabled(self):
        self.assertTrue(self.autocomplete.autocompletion_enabled(self.script))

    def test_autocompletion_enabled_fail(self):
        self.assertFalse(self.autocomplete.autocompletion_enabled(['']))
