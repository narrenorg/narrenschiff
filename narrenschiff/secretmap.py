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
import re
import sys
import uuid
import shutil
import difflib
import tempfile
import subprocess
from contextlib import suppress

import yaml
import click

from narrenschiff.chest import AES256Cipher
from narrenschiff.common import Singleton
from narrenschiff.common import DeleteFile
from narrenschiff.log import NarrenschiffLogger


logger = NarrenschiffLogger()


class CourseLocationError(Exception):
    """Raise exception if course is not found."""

    pass


class Secretmap(metaclass=Singleton):
    """Manage secret maps. Secret maps are paths to encrypted files."""

    FILENAME = 'secretmap.yaml'

    def __init__(self, keychain, directory):
        """
        Construct a :class:`narrenschiff.secretmap.Secretmap`.

        :param keychain: Keychain contains key and spice
        :type keychain: :class:`narrenschiff.chest.Keychain`
        :param directory: Path to directory containing secretmap
        :type directory: ``str``
        :return: Void
        :rtype: ``None``
        """
        if os.path.isfile(directory):
            self.directory = os.path.dirname(directory)
        elif os.path.isdir(directory):
            self.directory = directory
        else:
            raise CourseLocationError

        self.filepath = os.path.join(directory, Secretmap.FILENAME)
        self.keychain = keychain
        self.tmp = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))

    def upsert(self, src, dest, treasure):
        """
        Encrypts file and inserts data to config file.

        :param src: Source filepath for encryption
        :type src: ``str``
        :param dest: Destination filepath of the encrypted file
        :type dest: ``str``
        :param treasure: Name of the variable
        :type treasure: ``str``
        :return: Void
        :rtype: ``None``
        """
        with open(src, 'r') as f:
            cipher = AES256Cipher(self.keychain)
            enc_file_core = cipher.encrypt(f.read()).decode('utf-8')

        dest_abspath = os.path.abspath(os.path.join(self.directory, dest))
        try:
            os.makedirs(os.path.dirname(dest_abspath), 0o755)
        except FileExistsError:
            pass

        with open(dest_abspath, 'w') as f:
            f.write(enc_file_core)

        config = self._read_config()
        config[treasure] = dest
        self._write_config(config)

    def decrypt(self, dest, treasure):
        """
        Decrypts file and stores it to given destination.

        :param dest: Destination filepath of the decrypted file
        :type dest: ``str``
        :param treasure: Name of the variable
        :type treasure: ``str``
        :return: Void
        :rtype: ``None``
        """
        with open(dest, 'w') as f:
            f.write(self._decrypt(treasure))

    def peek(self, treasure):
        """
        Print encrypted file to STDOUT.

        :param treasure: Name of the secretmap variable
        :type treasure: ``str``
        :return: Void
        :rtype: ``None``
        """
        click.echo(self._decrypt(treasure))

    def find(self, match, treasure):
        """
        Match a pattern in a treasure and print to STDOUT.

        :param match: Pattern to match
        :type match: ``str``
        :param treasure: Name of the secretmap variable
        :type treasure: ``str``
        :return: Void
        :rtype: ``None``
        """
        secretmap = self._decrypt(treasure).split('\n')

        logger.debug(f'Searching for "{match}"')
        for index, line in enumerate(secretmap, start=1):
            candidate = re.search(match, line)
            if candidate:
                result = candidate.group()
                prefix = (f'\033[35m{treasure}\033[0m:\033[32m{index}\033[0m')
                formatted = line.replace(result, f'\033[31m{result}\033[0m')
                print(f'{prefix}:{formatted}')

    def diff(self, secretmaps):
        """
        Compare secretmaps line by line.

        :param secretmaps: Two secretmaps that should be compared
        :type secretmaps: ``tuple``
        :return: Void
        :rtype: ``None``
        """
        differences = difflib.unified_diff(
            self._decrypt(secretmaps[0]).splitlines(keepends=True),
            self._decrypt(secretmaps[1]).splitlines(keepends=True),
            fromfile=secretmaps[0],
            tofile=secretmaps[1]
        )

        for difference in differences:
            if difference.startswith('-'):
                click.secho(difference, nl=False, fg='red')
            elif difference.startswith('+'):
                click.secho(difference, nl=False, fg='green')
            else:
                click.secho(difference, nl=False)

    def destroy(self, treasure):
        """
        Delete secretmap file and remove key from the config file.

        :param treasure: Name of the secretmap variable
        :type treasure: ``str``
        :return: Void
        :rtype: ``None``
        """
        config = self._read_config()
        src = self._get_treasure_path(treasure)

        del config[treasure]
        self._write_config(config)
        os.remove(src)

    def render_all_files(self):
        """
        Decrypt and copy all files at the given destination.
        """
        os.makedirs(self.tmp)
        for key, value in self._read_config().items():
            basepath = os.path.dirname(value)

            with suppress(FileExistsError):
                os.makedirs(os.path.join(self.tmp, basepath))

            destination = os.path.join(self.tmp, value)
            if not os.path.exists(destination):
                self.decrypt(destination, key)

    def clear_all_files(self):
        """
        Delete all decrypted files.

        :return: Void
        :rtype: ``None``
        """
        logger.info(f'Deleting rendered secretmaps at {self.tmp}')
        shutil.rmtree(self.tmp)
        logger.info('Done!')

    def edit(self, treasure):
        """
        Edit an encrypted file.

        :param treasure: Name of the variable
        :type treasure: ``str``
        :return: Void
        :rtype: ``None``
        """
        config = self._read_config()
        filename = os.path.basename(config[treasure])
        destination = os.path.join(tempfile.gettempdir(), filename)
        self.decrypt(destination, treasure)

        editor = os.getenv('EDITOR', 'vi')
        cmd = '{} {}'.format(editor, destination)
        subprocess.run(cmd, shell=True)

        with open(destination, 'r') as f:
            tmp_file_content = f.read()

        src = self._get_treasure_path(treasure)
        with open(src, 'r') as f:
            cipher = AES256Cipher(self.keychain)
            original_file_content = cipher.decrypt(f.read())

        if original_file_content != tmp_file_content:
            self.upsert(destination, config[treasure], treasure)

        tmp_file = DeleteFile(destination)
        tmp_file.delete()

    def _get_treasure_path(self, treasure):
        """
        Get path to treasure from config file.

        :param treasure: Name of the treasure
        :type treasure: ``str``
        :return: Path to encrypted secretmap file
        :rtype: ``str``
        """
        config = self._read_config()
        try:
            return os.path.abspath(
                os.path.join(self.directory, config[treasure])
            )
        except KeyError:
            click.secho(
                f'Treasure "{treasure}" not found in {self.filepath}',
                fg='red'
            )
            sys.exit(1)

    def _read_config(self):
        """
        Load config file from the filesystem.

        :return: Content of the config file
        :rtype: ``dict``
        """
        try:
            with open(self.filepath, 'r') as f:
                config = yaml.safe_load(f)
        except FileNotFoundError:
            click.secho(f'File {self.filepath} not found', fg='red')
            sys.exit(1)
        return config if config else {}

    def _write_config(self, config):
        """
        Write config file to filesystem as YAML file.

        :param config: Content of the config file
        :type config: ``dict``
        :return: Void
        :rtype: ``None``
        """
        with open(self.filepath, 'w') as f:
            f.write(yaml.dump(config))

    def _decrypt(self, treasure):
        """
        Decrypt treasure, and return it as a cleartext string.

        :param treasure: Name of the treasure
        :type treasure: ``str``
        :return: Cleartext string
        :rtype: ``str``
        """
        src = self._get_treasure_path(treasure)

        with open(src, 'r') as f:
            logger.debug(f'Decrypting secretmap on {src}')
            cipher = AES256Cipher(self.keychain)
            secretmap = cipher.decrypt(f.read())

        return secretmap
