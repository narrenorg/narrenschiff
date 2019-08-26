import click

from narrenschiff.chest import Keychain
from narrenschiff.secretmap import SecretmapCommand


@click.group()
@click.pass_context
def secretmap(ctx):
    """
    Load keys and spices.

    :return: Void
    :rtype: ``None``
    """
    ctx.obj = Keychain()


@secretmap.command()
@click.option('--source', help='Source filepath for encryption')
@click.option('--destination', help='Destination of the encrypted file')
@click.option('--treasure', help='Variable name')
@click.option('--location', help='Relative path to course project directory')
@click.pass_obj
def stash(keychain, source, destination, treasure, location):
    """
    Encrypt and stash file.

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
    secretmap = SecretmapCommand(keychain=keychain, directory=location)
    secretmap.upsert(src=source, dest=destination, treasure=treasure)


@secretmap.command()
@click.option('--destination', help='Destination of the encrypted file')
@click.option('--treasure', help='Variable name')
@click.option('--location', help='Relative path to course project directory')
@click.pass_obj
def loot(keychain, destination, treasure, location):
    """
    Decrypt file from stash.

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

    secretmap = SecretmapCommand(keychain=keychain, directory=location)
    secretmap.decrypt(dest=destination, treasure=treasure)
