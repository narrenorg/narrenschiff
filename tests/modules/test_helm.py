import unittest
from unittest import mock

from narrenschiff.modules.helm import Helm


@mock.patch(
    'narrenschiff.modules.helm.Secretmap',
    mock.MagicMock(
        return_value=type('S', (), {'tmp': '/tmp/nonexistent'})
    )
)
class HelmTestCase(unittest.TestCase):

    def setUp(self):
        self.helm = Helm({
            'command': 'upgrade',
            'name': 'release',
            'chart': 'repo/chart',
            'opts': [
                'install',
            ],
            'args': {
                'namespace': 'default',
                'version': '1.0.0',
                'values': [
                    '{{secretmap}}/values.yaml'
                ],
                'set': [
                    'key=val'
                ]
            }
        })

    def test_cmd(self):
        expected = ('helm upgrade release repo/chart --install '
                    '--namespace default --version 1.0.0 '
                    '--values /tmp/nonexistent/values.yaml --set key=val')
        self.assertEqual(self.helm.cmd, expected)

    def test_cmd_without_set(self):
        helm = Helm({
            'command': 'upgrade',
            'name': 'release',
            'chart': 'repo/chart',
            'opts': [
                'install',
            ],
            'args': {
                'namespace': 'default',
                'version': '1.0.0',
                'values': [
                    '{{secretmap}}/values.yaml'
                ],
            }
        })
        expected = ('helm upgrade release repo/chart --install '
                    '--namespace default --version 1.0.0 '
                    '--values /tmp/nonexistent/values.yaml ')
        self.assertEqual(helm.cmd, expected)

    def test_cmd_without_opts(self):
        helm = Helm({
            'command': 'upgrade',
            'name': 'release',
            'chart': 'repo/chart',
            'args': {
                'namespace': 'default',
                'version': '1.0.0',
                'values': [
                    '{{secretmap}}/values.yaml'
                ],
            }
        })
        expected = ('helm upgrade release repo/chart  '
                    '--namespace default --version 1.0.0 '
                    '--values /tmp/nonexistent/values.yaml ')
        self.assertEqual(helm.cmd, expected)

    def test_cmd_without_opts_and_args(self):
        helm = Helm({'command': 'repo update'})
        expected = ('helm repo update     ')
        self.assertEqual(helm.cmd, expected)

    def test_parse_secretmaps_args(self):
        self.helm.parse_secretmaps_args()
        self.assertEqual(
            self.helm.command.get('args')['values'][0],
            '/tmp/nonexistent/values.yaml'
        )

    def test_dry_run_supported(self):
        self.assertTrue(
            self.helm.dry_run_supported(
                'helm install prometheus prometheus-community/prometheus'
            )
        )

    def test_dry_run_not_supported(self):
        self.assertFalse(self.helm.dry_run_supported('helm version'))

    def tearDown(self):
        self.helm = None
