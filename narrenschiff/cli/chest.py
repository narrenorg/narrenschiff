import click

from narrenschiff.chest import Keychain


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
@click.option('--value', help='Value')
@click.pass_obj
def take(keychain, treasure, value):
    """
    Display value from the chest file.

    :param treasure: Name of the variable
    :type treasure: ``str``
    :param value: Value of the variable
    :type value: ``str``
    :return: Void
    :rtype: ``None``
    """
    pass


@chest.command()
@click.option('--treasure', help='Variable name')
@click.option('--value', help='Value')
@click.pass_obj
def hide(keychain, treasure, value):
    """
    Dynamically update chest file.

    :param treasure: Name of the variable
    :type treasure: ``str``
    :param value: Value of the variable
    :type value: ``str``
    :return: Void
    :rtype: ``None``
    """
    pass
