import click

from narrenschiff.cli.deploy import deploy
from narrenschiff.cli.chest import chest


@click.group()
def narrenschiff():
    """
    Base command.

    :return: Void
    :rtype: ``None``
    """
    pass


narrenschiff.add_command(deploy)
narrenschiff.add_command(chest)
