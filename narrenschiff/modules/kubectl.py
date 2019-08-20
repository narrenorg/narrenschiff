import os
from contextlib import suppress

from narrenschiff.modules.common import NarrenschiffModule


class Kubectl(NarrenschiffModule):
    """``kubectl`` module."""

    kubectl = 'kubectl'

    # TODO: Implement templating (echo -e 'lorem\n  ipsum' | cat - | kubectl -)
    def execute(self):
        command = self.command.get('command')

        self.sanitize_filenames()
        self.update_filename_argument()
        args = self.command.get('args')
        flags = []
        for key in args:
            flags.append("--{} '{}'".format(key, args[key]))

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

    def sanitize_filenames(self):
        """
        Change relative paths to absolute paths corresponding to rendered
        files.

        :return: Void
        :rtype: ``None``
        """
        try:
            filename = self.command['args']['filename']
            path = os.path.join(self.template.tmp, filename)
            self.command['args']['filename'] = path
        except TypeError:
            filenames = self.command['args']['filename']
            paths = []
            for filename in filenames:
                paths.append(os.path.join(self.template.tmp, filename))
            self.command['args']['filename'] = paths
        except KeyError:
            pass
