import os
import subprocess
from contextlib import suppress

from narrenschiff.modules.common import NarrenschiffModule
from narrenschiff.secretmap import Secretmap


class Helm(NarrenschiffModule):
    """``helm`` module."""

    helm_cmd = 'helm'

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

        args = ' '.join(
            ['--{} {}'.format(key, value)
                for key, value in arguments.items()
                if key != 'set']
        )

        sets = ''
        if args_set:
            sets = ' '.join(['--set {}'.format(s) for s in args_set])

        cmd = ' '.join([Helm.helm_cmd, command, chart, opts, args, sets])
        subprocess.run(cmd, shell=True, check=True)

    def parse_secretmaps_args(self):
        """
        Mutate secretmap arguments. Expand secretmap paths to match files in
        the ``/tmp`` directory.

        :return: Void
        :rtype: ``None``
        """
        secretmap = '{{secretmap}}/'
        for key, value in self.command.get('args', {}).items():
            with suppress(AttributeError):
                if value.startswith(secretmap):
                    basepath = value.replace(secretmap, '')
                    tmp = Secretmap().tmp
                    rendered_path = os.path.join(tmp, basepath)
                    self.command['args'][key] = rendered_path
