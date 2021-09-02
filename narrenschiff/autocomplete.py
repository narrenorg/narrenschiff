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


class ShellAutocomplete:
    """Set autocompletion."""

    AUTOCOMPLETION_START_TAG = '### narrenschiff-autocompletion-start ###\n'
    AUTOCOMPLETION_END_TAG = '### narrenschiff-autocompletion-end ###\n'

    def autocompletion_script(self):
        """
        Return autocompletion script.

        :return: Autocompletion script
        :rtype: ``list`` of ``str``
        """
        return ''.join([
            '\n\n',
            ShellAutocomplete.AUTOCOMPLETION_START_TAG,
            'eval "$(_NARRENSCHIFF_COMPLETE=source_bash narrenschiff)"\n',
            ShellAutocomplete.AUTOCOMPLETION_END_TAG
        ])

    def get_config_file(self):
        """
        Get type of the config file.

        :return: Name of the config file
        :rtype: ``str``

        This method returns either ``.bashrc`` (which will later be edited for
        the current user), or ``activate`` which symbolises activate script of
        your virtualenv.
        """
        if os.getenv('VIRTUAL_ENV'):
            return os.getenv('VIRTUAL_ENV'), 'bin/activate'
        return '~', '.bashrc'

    def get_abs_path(self, *args):
        """
        Join arguments, and return absolute path.

        :param args: Paths to be joined
        :type args: ``list`` of ``str``
        :return: Absolute path
        :rtype: ``str``

        If the first argument is tilde (~) then the method will expand user.
        """
        if args[0] == '~':
            return os.path.join(os.path.expanduser('~'), *args[1:])
        return os.path.join(*args)

    def read_file(self, path):
        """
        Read configuration file.

        :param path: Path to the file to read
        :type path: ``str``
        :return: File as a list
        :rtype: ``list`` of ``str``
        """
        with open(path, 'r') as f:
            return f.readlines()

    def autocompletion_enabled(self, config):
        """
        Check if the file contains the autocompletion tag.

        :param config: Configuration file
        :type config: ``list`` of ``str``
        :return: Confirmation whether file contains autocompletion tag
        :rtype: ``bool``
        """
        if ShellAutocomplete.AUTOCOMPLETION_START_TAG in config:
            return True
        return False

    def add_autocompletion(self, path):
        """
        Add autocompletion to the config file.

        :param path: Path to configuration file
        :type path: ``str``
        :return: Void
        :rtype: ``None``
        """
        config = self.read_file(path)
        if not self.autocompletion_enabled(config):
            with open(path, 'a') as f:
                f.write(self.autocompletion_script())

    def add(self):
        """
        Add narrenschiff autocomplete to shell config.

        :return: Void
        :rtype: ``None``
        """
        path, cnftype = self.get_config_file()
        config_path = self.get_abs_path(path, cnftype)
        self.add_autocompletion(config_path)
