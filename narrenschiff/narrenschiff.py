import click
import yaml

from narrenschiff.task import Task


@click.group()
def narrenschiff():
    pass


@narrenschiff.command()
@click.option('--chart', help='Path to your YAML chart.')
def deploy(chart):
    # Load tasks file
    with open(chart, 'r') as f:
        tasks = yaml.load(f, Loader=yaml.FullLoader)

    tasks = [Task(task).command for task in tasks]
    click.echo(tasks)
