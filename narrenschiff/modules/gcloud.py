import subprocess

from narrenschiff.modules.common import NarrenschiffModule


class Gcloud(NarrenschiffModule):
    """``gcloud`` module."""

    gcloud_cmd = 'gcloud'

    def execute(self):
        command = self.command.get('command')
        args = self.command.get('args', {})
        switches = self.command.get('opts', [])

        flags = []
        for flag, value in args.items():
            flags.append("--{} '{}'".format(flag, args[flag]))

        flags.extend(['--{}'.format(switch) for switch in switches])

        cmd = ' '.join([Gcloud.gcloud_cmd, command, *flags])

        # When you enable some API the output will be empty
        # It's OK to pipe to stdout instead of catching with check in the
        # tasks engine - though it would create problems with commands that
        # require user input
        subprocess.run(cmd, shell=True, check=True)
