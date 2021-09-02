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
import click

from narrenschiff.config import Keychain
from narrenschiff.templating import SecretmapVars
from narrenschiff.secretmap import Secretmap
from narrenschiff.secretmap import CourseLocationError


@click.group()
@click.pass_context
def secretmap(ctx):
    """
    Encrypt, decrypt, and edit files.
    \f

    :return: Void
    :rtype: ``None``
    """
    ctx.obj = Keychain()


@secretmap.command()
@click.option('--source', help='Source filepath for encryption.')
@click.option(
    '--destination',
    help=('Destination of the encrypted file.'
          ' Path relative to course project directory.')
)
@click.option('--treasure', help='Variable name.')
@click.option('--location', help='Relative path to course project directory.')
@click.pass_obj
def stash(keychain, source, destination, treasure, location):
    """
    Encrypt and stash file.
    \f

    :param keychain: Object containing key and spice
    :type keychain: :class:`narrenschiff.chest.Keychain`
    :param source: Source filepath for encryption
    :type source: ``str``
    :param destination: Destination filepath of the encrypted file
    :type destination: ``str``
    :param treasure: Name of the variable
    :type treasure: ``str``
    :param location: Location of the secretmap file
    :type location: ``str``
    :return: Void
    :rtype: ``None``
    """
    secretmap = Secretmap(keychain=keychain, directory=location)
    secretmap.upsert(src=source, dest=destination, treasure=treasure)


@secretmap.command()
@click.option('--destination', help='Destination of the encrypted file.')
@click.option('--treasure', help='Variable name.')
@click.option('--location', help='Relative path to course project directory.')
@click.pass_obj
def loot(keychain, destination, treasure, location):
    """
    Decrypt file from stash.
    \f

    :param keychain: Object containing key and spice
    :type keychain: :class:`narrenschiff.chest.Keychain`
    :param destination: Destination filepath of the decrypted file
    :type destination: ``str``
    :param treasure: Name of the variable
    :type treasure: ``str``
    :param location: Location of the secretmap file
    :type location: ``str``
    :return: Void
    :rtype: ``None``
    """
    secretmap = Secretmap(keychain=keychain, directory=location)
    secretmap.decrypt(dest=destination, treasure=treasure)


@secretmap.command()
@click.option('--treasure', help='Variable name from the secretmap file.')
@click.option('--location', help='Relative path to course project directory.')
@click.pass_obj
def peek(keychain, treasure, location):
    """
    Print content of the encrypted file to STDOUT.
    \f

    :param keychain: Object containing key and spice
    :type keychain: :class:`narrenschiff.chest.Keychain`
    :param treasure: Name of the variable
    :type treasure: ``str``
    :param location: Location of the secretmap file
    :type location: ``str``
    :return: Void
    :rtype: ``None``
    """
    secretmap = Secretmap(keychain=keychain, directory=location)
    secretmap.peek(treasure)


@secretmap.command()
@click.option(
    '--treasure',
    help='Variable name from the secretmap file of the file you want to edit.'
)
@click.option('--location', help='Relative path to course project directory.')
@click.pass_obj
def alter(keychain, treasure, location):
    """
    Decrypt and edit the file. After edits, the file is encrypted again.
    \f

    :param keychain: Object containing key and spice
    :type keychain: :class:`narrenschiff.chest.Keychain`
    :param treasure: Name of the variable
    :type treasure: ``str``
    :param location: Location of the secretmap file
    :type location: ``str``
    :return: Void
    :rtype: ``None``
    """
    secretmap = Secretmap(keychain=keychain, directory=location)
    secretmap.edit(treasure)


@secretmap.command()
@click.option('--treasure', help='Variable name from the secretmap file.')
@click.option('--location', help='Relative path to course project directory.')
@click.pass_obj
def destroy(keychain, treasure, location):
    """
    Delete secretmap file and corresponding key in the secretmap.
    \f

    :param keychain: Object containing key and spice
    :type keychain: :class:`narrenschiff.chest.Keychain`
    :param treasure: Name of the variable
    :type treasure: ``str``
    :param location: Location of the secretmap file
    :type location: ``str``
    :return: Void
    :rtype: ``None``

    **You cannot undo this action!**
    """
    secretmap = Secretmap(keychain=keychain, directory=location)
    secretmap.destroy(treasure)


@secretmap.command()
@click.option('--location', help='Relative path to course project directory.')
@click.option('--match', help='Pattern you are searching for.')
@click.pass_obj
def search(keychain, location, match):
    """
    Search for a pattern in secretmaps.
    \f

    :param keychain: Object containing key and spice
    :type keychain: :class:`narrenschiff.chest.Keychain`
    :param location: Location of the secretmap file
    :type location: ``str``
    :param match: Pattern you are looking for
    :type match: ``str``
    :return: Void
    :rtype: ``None``
    """
    if not os.path.isdir(location):
        raise CourseLocationError

    vars = SecretmapVars(location).load_vars()

    for treasure in vars[0].keys():
        secretmap = Secretmap(keychain=keychain, directory=location)
        secretmap.find(match, treasure)


@secretmap.command()
@click.option('--location', help='Relative path to course project directory.')
@click.argument('secretmaps', nargs=2)
@click.pass_obj
def diff(keychain, location, secretmaps):
    """
    Compare secretmaps line by line.

    It can only compare secretmaps in the same course project.
    \f

    :param location: Location of the secretmap file
    :type location: ``str``
    :param secretmaps: Two secretmaps that should be compared
    :type secretmaps: ``str``
    :return: Void
    :rtype: ``None``
    """
    secretmap = Secretmap(keychain=keychain, directory=location)
    secretmap.diff(secretmaps)
