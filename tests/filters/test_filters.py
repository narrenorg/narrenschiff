import unittest

from narrenschiff.filters import filters


class FiltersTestCase(unittest.TestCase):

    def test_base64(self):
        self.assertEqual('dGVzdA==', filters['b64enc']('test'))

    def test_rtrim(self):
        self.assertEqual('value', filters['rtrim']('value     '))

    def test_secretmap(self):
        self.assertEqual('{{secretmap}}/test', filters['secretmap']('test'))
