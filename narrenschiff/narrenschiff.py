import click

from narrenschiff.cli.deploy import deploy
from narrenschiff.cli.chest import chest
from narrenschiff.cli.secretmap import secretmap
from narrenschiff.log import NarrenschiffLogger


@click.group()
@click.option(
    '--verbosity',
    'verbosity',
    required=False,
    type=int,
    help='Set verbosity (levels available are from 1 to 5)')
def narrenschiff(verbosity=0):
    """
    Base command.

    :return: Void
    :rtype: ``None``
    """
    logger = NarrenschiffLogger()
    logger.set_verbosity(verbosity)


narrenschiff.add_command(secretmap)
narrenschiff.add_command(deploy)
narrenschiff.add_command(chest)
