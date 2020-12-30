import os
from contextlib import suppress
from urllib.parse import urlparse

from narrenschiff.common import flatten
from narrenschiff.modules.common import NarrenschiffModule
from narrenschiff.templating import Template


class Kubectl(NarrenschiffModule):
    """``kubectl`` module."""

    @property
    def cmd(self):
        command = self.command.get('command')
        switches = self.command.get('opts', [])

        self.sanitize_filenames()
        self.update_filename_argument()
        args = self.command.get('args', {})
        flags = []
        for key, value in args.items():
            flags.append("--{}='{}'".format(key, value))

        flags.extend(['--{}'.format(switch) for switch in switches])

        return ' '.join(['kubectl', command, *flags])

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
        with suppress(KeyError):
            filenames = flatten(list((self.command['args']['filename'],)))

            paths = []
            for filename in filenames:
                if urlparse(filename).scheme:
                    paths.append(filename)
                    continue
                paths.append(os.path.join(Template().tmp, filename))

            self.command['args']['filename'] = paths

    @property
    def dry_run(self):
        return '--dry-run=server'  # none, server, client, -o yaml

    def dry_run_supported(self, cmd):
        whitelist = [
            'run',
            'apply',
            'delete',
            'create',
            'scale',
            'autoscale',
            'patch',
            'replace',
        ]

        if cmd.split()[1] in whitelist:
            return True
        return False
