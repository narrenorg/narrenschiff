import os
import subprocess
from contextlib import suppress

import click

from narrenschiff.modules.common import NarrenschiffModule


class Kubectl(NarrenschiffModule):
    """``kubectl`` module."""

    kubectl = 'kubectl'

    # This should probably be class with consts
    # color = {
    #     'changed': 'yellow',
    #     'ok': 'green'
    # }

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

        process = subprocess.run(
            cmd,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        output = process.stdout if process.stdout else process.stderr
        color = 'green' if process.stdout else 'red'
        click.secho(output.decode('utf-8'), fg=color)

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