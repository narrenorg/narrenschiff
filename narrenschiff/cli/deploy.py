import os

import click
import yaml

from narrenschiff.task import Task
from narrenschiff.task import TasksEngine
from narrenschiff.templating import Template


@click.command()
@click.option('--set-course', 'course', help='Path to your YAML course file.')
def deploy(course):
    """
    Turn tasks into actions.

    :param course: The path to ``course`` file. A file containing tasks
        specified in the YAML format. Tasks are ``executable`` pieces of
        configuration. Course is Jinja2 templated file (as are all the
        kubernetes manifest files)
    :type course: ``str``
    :return: Void
    :rtype: ``None``
    """
    # Load and template tasks files
    template = Template(course)
    tasks_raw = template.render(os.path.basename(course))
    tasks = yaml.load(tasks_raw, Loader=yaml.FullLoader)

    template.render_all_files()
    template.clear_templates()
    # engine = TasksEngine([Task(task, template) for task in tasks])
    # engine.run()
