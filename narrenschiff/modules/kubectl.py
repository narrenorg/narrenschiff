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
from urllib.parse import urlparse

from narrenschiff.common import flatten
from narrenschiff.templating import Template
from narrenschiff.modules.mixins import KubectlDryRunMixin
from narrenschiff.modules.common import NarrenschiffModule


class Kubectl(KubectlDryRunMixin, NarrenschiffModule):
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
