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
    # Load tasks file
    with open(chart, 'r') as f:
        tasks = yaml.load(f, Loader=yaml.FullLoader)

    template = Template(chart)
    click.echo(template.load_vars())
    # Load task files
    # Template tasks files
    # Individual task will call template endinge for the given dir or file

    # tasks = [Task(task).command for task in tasks]
    # click.echo(tasks)
