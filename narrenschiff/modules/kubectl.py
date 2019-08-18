from contextlib import suppress
from narrenschiff.modules.common import NarrenschiffModule


class Kubectl(NarrenschiffModule):
    """``kubectl`` module."""

    kubectl = 'kubectl'

    # TODO: Implement templating (echo -e 'lorem\n  ipsum' | cat - | kubectl -)
    def execute(self):
        command = self.command.get('command')

        self.update_filename_argument()
        args = self.command.get('args')
        flags = []
        for key in args:
            flags.append('--{} "{}"'.format(key, args[key]))

        cmd = ' '.join([Kubectl.kubectl, command, *flags])
        print(cmd)

    def update_filename_argument(self):
        """
        Update filename argument as a properly formated string.

        :return: Void
        :rtype: ``None``
        """
        with suppress(KeyError):
            filenames = self.command['args']['filename']
            if isinstance(filenames, list):
                self.command['args']['filename'] = ','.join(filenames)
