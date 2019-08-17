import os

import click
import yaml

from narrenschiff.task import Task
from narrenschiff.templating import Template


@click.group()
def narrenschiff():
    pass


@narrenschiff.command()
@click.option('--chart', help='Path to your YAML chart.')
def deploy(chart):
    template = Template(chart)
    tasks_raw = template.render(os.path.basename(chart))
    tasks = yaml.load(tasks_raw, Loader=yaml.FullLoader)
    click.echo(tasks)
    # Load task files
    # Template tasks files
    # Individual task will call template endinge for the given dir or file

    # tasks = [Task(task).command for task in tasks]
    # click.echo(tasks)
