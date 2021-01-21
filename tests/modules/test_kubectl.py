import unittest

from narrenschiff.templating import Template
from narrenschiff.modules.kubectl import Kubectl


class KubectlTestCase(unittest.TestCase):

    def setUp(self):
        Template().tmp = '/tmp/nonexistent'
        self.kubectl = Kubectl({
            'command': 'apply',
            'args': {
                'filename': [
                    'app/manifest.yaml',
                    'http://example.com/manifest.yaml'
                ]
            }
        })

    def test_sanitize_filenames(self):
        self.kubectl.sanitize_filenames()
        self.assertEqual(
            self.kubectl.command.get('args')['filename'][0],
            '/tmp/nonexistent/app/manifest.yaml'
        )
        self.assertEqual(
            self.kubectl.command.get('args')['filename'][1],
            'http://example.com/manifest.yaml'
        )

    def test_update_filename_argument(self):
        self.kubectl.sanitize_filenames()
        self.kubectl.update_filename_argument()
        self.assertEqual(
            self.kubectl.command.get('args')['filename'],
            ('/tmp/nonexistent/app/manifest.yaml,'
             'http://example.com/manifest.yaml')
        )

    def test_cmd(self):
        expected = "kubectl apply --filename='/tmp/nonexistent/app/manifest.yaml,http://example.com/manifest.yaml'"  # noqa
        self.assertEqual(self.kubectl.cmd, expected)

    def test_arg_with_str_filename(self):
        kubectl = Kubectl({
            'command': 'apply',
            'args': {
                'filename': 'http://example.com/manifest.yaml'
            }
        })
        expected = ("kubectl apply "
                    "--filename='http://example.com/manifest.yaml'")
        self.assertEqual(kubectl.cmd, expected)

    def tearDown(self):
        self.kubectl = None
