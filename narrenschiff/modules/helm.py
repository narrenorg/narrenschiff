from narrenschiff.modules.common import NarrenschiffModule
import subprocess


class Helm(NarrenschiffModule):
    """``Helm`` module."""

    helm_cmd = 'helm'

    def execute(self):
        command = self.command.get('command')
        chart = self.command.get('chart')

        opts_str = ' '.join(map(lambda opt: '--{}'.format(opt) , self.command.get('opts')))

        args_str = ' '.join([ '--{} {}'.format(key, value) for key, value in self.command.get('args').items()])

        sets = self.command.get('args').get('set')
        # print(sets)
        sets_str = ' '.join(['--set {}'.format(s) for s in sets])
            
        # print(self.command)

        cmd = ' '.join([Helm.helm_cmd, command, chart, opts_str, args_str, sets_str])
        print(cmd)
        # subprocess.check_call(cmd, shell=True)
