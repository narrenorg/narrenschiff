import click

from narrenschiff.chest import Chest
from narrenschiff.chest import Keychain
from narrenschiff.chest import AES256Cipher

from narrenschiff.common import get_chest_file_path


@click.group()
@click.pass_context
def chest(ctx):
    """
    Load keys and spices.

    :return: Void
    :rtype: ``None``
    """
    ctx.obj = Keychain()


@chest.command()
@click.option('--treasure', help='Variable name')
@click.option('--location', help='Relative path to course project directory')
@click.pass_obj
def loot(keychain, treasure, location):
    """
    Display value from the chest file.

    :param keychain: Object containing key and spice
    :type keychain: :class:`narrenschiff.chest.Keychain`
    :param treasure: Name of the variable
    :type treasure: ``str``
    :return: Void
    :rtype: ``None``
    """
    path = get_chest_file_path(location)
    chest = Chest(keychain, path)
    click.echo(chest.show(treasure))


@chest.command()
@click.option('--treasure', help='Variable name')
@click.option('--value', help='Value')
@click.option('--location', help='Relative path to course project directory')
@click.pass_obj
def stash(keychain, treasure, value, location):
    """
    Dynamically update chest file. Override old value if exists.

    :param keychain: Object containing key and spice
    :type keychain: :class:`narrenschiff.chest.Keychain`
    :param treasure: Name of the variable
    :type treasure: ``str``
    :param value: Value of the variable
    :type value: ``str``
    :return: Void
    :rtype: ``None``
    """
    path = get_chest_file_path(location)
    chest = Chest(keychain, path)
    chest.update(treasure, value)


@chest.command()
@click.option('--value', help='String to be encrypted')
@click.pass_obj
def lock(keychain, value):
    """
    Encrypt string and print it to STDOUT.

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
@click.option('--value', help='String to be decrypted')
@click.pass_obj
def unlock(keychain, value):
    """
    Decrypt string and print it to STDOUT.

    :param keychain: Object containing key and spice
    :type keychain: :class:`narrenschiff.chest.Keychain`
    :param value: Value of the variable
    :type value: ``str``
    :return: Void
    :rtype: ``None``
    """
    cipher = AES256Cipher(keychain)
    click.echo(cipher.decrypt(value))
