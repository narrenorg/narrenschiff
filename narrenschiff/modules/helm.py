# Copyright 2021 The Narrenschiff Authors

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from contextlib import suppress

from narrenschiff.modules.common import NarrenschiffModule
from narrenschiff.secretmap import Secretmap


class HelmException(Exception):
    """Raise when something is wrong with Helm module."""

    pass


class Helm(NarrenschiffModule):
    """``helm`` module."""

    @property
    def cmd(self):
        command = self.command.get('command')
        name = self.command.get('name', '')
        chart = self.command.get('chart', '')
        options = self.command.get('opts', [])
        arguments = self.command.get('args', {})

        self.parse_secretmaps_args()

        try:
            args_set = self.command.get('args').get('set')
        except AttributeError:
            args_set = None

        opts = ''
        if options:
            opts = ' '.join(map(lambda opt: '--{}'.format(opt), options))

        with suppress(AttributeError, TypeError):
            values = ','.join(self.command.get('args').get('values'))
            self.command['args']['values'] = values

        args = ' '.join(
            ['--{} {}'.format(key, value)
                for key, value in arguments.items()
                if key != 'set']
        )

        sets = ''
        if args_set:
            sets = ' '.join(['--set {}'.format(s) for s in args_set])

        return ' '.join(['helm', command, name, chart, opts, args, sets])

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

    def dry_run_supported(self, cmd):
        whitelist = [
            'install',
            'template',
            'uninstall',
            'upgrade',
        ]

        if cmd.split()[1] in whitelist:
            return True
        return False
