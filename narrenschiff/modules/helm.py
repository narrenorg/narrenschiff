import subprocess

from narrenschiff.modules.common import NarrenschiffModule


class Helm(NarrenschiffModule):
    """``helm`` module."""

    helm_cmd = 'helm'

    def execute(self):
        command = self.command.get('command')
        chart = self.command.get('chart', '')
        options = self.command.get('opts')
        arguments = self.command.get('args', {})

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
        subprocess.run(cmd, shell=True, check=Trye)
