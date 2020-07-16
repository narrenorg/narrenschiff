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
