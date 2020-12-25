from narrenschiff.modules.common import NarrenschiffModule


class Gcloud(NarrenschiffModule):
    """``gcloud`` module."""

    @property
    def cmd(self):
        command = self.command.get('command')
        args = self.command.get('args', {})
        switches = self.command.get('opts', [])

        flags = []
        for flag, value in args.items():
            flags.append("--{} '{}'".format(flag, args[flag]))

        flags.extend(['--{}'.format(switch) for switch in switches])

        return ' '.join(['gcloud', command, *flags])
