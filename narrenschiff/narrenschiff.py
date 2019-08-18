import click

from narrenschiff.cli.deploy import deploy


@click.group()
def narrenschiff():
    """
    Base command.

    :return: Void
    :rtype: ``None``
    """
    pass


narrenschiff.add_command(deploy)
