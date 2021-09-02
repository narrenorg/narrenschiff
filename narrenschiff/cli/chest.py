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

from narrenschiff.chest import Chest
from narrenschiff.chest import AES256Cipher
from narrenschiff.config import Keychain

from narrenschiff.common import get_chest_file_path
from narrenschiff.templating import ChestVars
from narrenschiff.secretmap import CourseLocationError


@click.group()
@click.pass_context
def chest(ctx):
    """
    Load keys and spices.
    \f

    :return: Void
    :rtype: ``None``
    """
    ctx.obj = Keychain()


@chest.command()
@click.option('--treasure', help='Variable name.')
@click.option('--location', help='Relative path to course project directory.')
@click.pass_obj
def loot(keychain, treasure, location):
    """
    Display value from the chest file.
    \f

    :param keychain: Object containing key and spice
    :type keychain: :class:`narrenschiff.chest.Keychain`
    :param treasure: Name of the variable
    :type treasure: ``str``
    :param location: Path to the course directory
    :type location: ``str``
    :return: Void
    :rtype: ``None``
    """
    path = get_chest_file_path(location)
    chest = Chest(keychain, path)
    click.echo(chest.show(treasure))


@chest.command()
@click.option('--treasure', help='Variable name.')
@click.option('--value', help='Value.')
@click.option('--location', help='Relative path to course project directory.')
@click.pass_obj
def stash(keychain, treasure, value, location):
    """
    Dynamically update chest file. Override old value if exists.
    \f

    :param keychain: Object containing key and spice
    :type keychain: :class:`narrenschiff.chest.Keychain`
    :param treasure: Name of the variable
    :type treasure: ``str``
    :param value: Value of the variable
    :type value: ``str``
    :param location: Path to the course directory
    :type location: ``str``
    :return: Void
    :rtype: ``None``
    """
    path = get_chest_file_path(location)
    chest = Chest(keychain, path)
    chest.update(treasure, value)


@chest.command()
@click.option('--value', help='String to be encrypted.')
@click.pass_obj
def lock(keychain, value):
    """
    Encrypt string and print it to STDOUT.
    \f

    :param keychain: Object containing key and spice
    :type keychain: :class:`narrenschiff.chest.Keychain`
    :param value: Value of the variable
    :type value: ``str``
    :return: Void
    :rtype: ``None``
    """
    cipher = AES256Cipher(keychain)
    click.echo(cipher.encrypt(value))


@chest.command()
@click.option('--value', help='String to be decrypted.')
@click.pass_obj
def unlock(keychain, value):
    """
    Decrypt string and print it to STDOUT.
    \f

    :param keychain: Object containing key and spice
    :type keychain: :class:`narrenschiff.chest.Keychain`
    :param value: Value of the variable
    :type value: ``str``
    :return: Void
    :rtype: ``None``
    """
    cipher = AES256Cipher(keychain)
    click.echo(cipher.decrypt(value))


@chest.command()
@click.option('--location', help='Relative path to course project directory.')
def dump(location):
    """
    Print all values from the chest on STDOUT.
    \f

    :param location: Path to the course directory
    :type location: ``str``
    :return: Void
    :rtype: ``None``
    """
    if not os.path.isdir(location):
        raise CourseLocationError

    vars = ChestVars(location).load_vars()

    for key, value in vars[0].items():
        print(f'{key}: {value}')
