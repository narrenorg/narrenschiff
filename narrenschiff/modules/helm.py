import os
import subprocess
from contextlib import suppress

from narrenschiff.modules.common import NarrenschiffModule
from narrenschiff.secretmap import Secretmap


class Helm(NarrenschiffModule):
    """``helm`` module."""

    helm = 'helm'

    def execute(self):
        command = self.command.get('command')
        chart = self.command.get('chart', '')
        options = self.command.get('opts')
        arguments = self.command.get('args', {})

        self.parse_secretmaps_args()

        try:
            args_set = self.command.get('args').get('set')
        except AttributeError:
            args_set = None

        opts = ''
        if options:
            opts = ' '.join(map(lambda opt: '--{}'.format(opt), options))

        try:
            values = ','.join(self.command.get('args').get('values'))
            self.command['args']['values'] = values
        except (AttributeError, TypeError):
            values = ''

        args = ' '.join(
            ['--{} {}'.format(key, value)
                for key, value in arguments.items()
                if key != 'set']
        )

        sets = ''
        if args_set:
            sets = ' '.join(['--set {}'.format(s) for s in args_set])

        cmd = ' '.join([Helm.helm, command, chart, opts, args, sets])
        subprocess.run(cmd, shell=True, check=True)

    def parse_secretmaps_args(self):
        """
        Mutate secretmap arguments. Expand secretmap paths to match files in
        the ``/tmp`` directory.

        :return: Void
        :rtype: ``None``
        """
        for key, value in self.command.get('args', {}).items():
            try:
                self.command['args'][key] = self._template_path(value)
            except AttributeError:
                if key == 'values':
                    values = [self._template_path(v) for v in value]
                    self.command['args'][key] = values

    def _template_path(self, value):
        """Replace secretmap filter artifact with `/tmp` file path."""
        secretmap = '{{secretmap}}/'
        if value.startswith(secretmap):
            basepath = value.replace(secretmap, '')
            tmp = Secretmap().tmp
            return os.path.join(tmp, basepath)
        return value
