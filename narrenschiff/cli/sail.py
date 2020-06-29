import os

import click
import yaml

from narrenschiff.task import Task
from narrenschiff.task import TasksEngine
from narrenschiff.templating import Template
from narrenschiff.chest import Keychain
from narrenschiff.secretmap import Secretmap


@click.command()
@click.option('--set-course', 'course', help='Path to your YAML course file.')
@click.option(
    '--follow-beacons',
    'beacons',
    required=False,
    type=str,
    help='Execute tasks marked only by given beacons (comma separated list).')
def sail(course, beacons):
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
    template = Template()
    template.set_course(course)

    secretmap = Secretmap(Keychain(), os.path.dirname(course))

    tasks = _import_course(course, template)

    template.render_all_files()
    secretmap.render_all_files()

    try:
        beacons = set(beacons.split(','))
    except AttributeError:
        beacons = set()

    engine = TasksEngine(tasks, beacons)
    engine.run()

    template.clear_templates()
    secretmap.clear_all_files()


def _import_course(course, template):
    """
    Recursively load all courses and return tasks.

    :param course: Path to the course file
    :type course: ``str``
    :param template: Template environment
    :type template: :class:`narrenschiff.templating.Template`
    :return: All tasks from the original, and the included course files
    :rtype: ``list`` of :class:`narrenschiff.task.Task`
    """
    tasks_yaml = _import_current_tasks(course, template)

    tasks = []
    for task in tasks_yaml:
        follow_course = task.get('import_course')
        if follow_course:
            new_tasks = _import_course(follow_course, template)
            for new_task in new_tasks:
                tasks.append(new_task)
        else:
            tasks.append(Task(task))

    return tasks


def _import_current_tasks(course, template):
    """
    Render tasks from the course.

    :param course: Path to the course file
    :type course: ``str``
    :param template: Template environment
    :type template: :class:`narrenschiff.templating.Template`
    :return: Tasks as a list of dictionaries
    :rtype: ``list`` of ``dict``
    """
    tasks_raw = template.render(os.path.basename(course))
    tasks_yaml = yaml.load(tasks_raw, Loader=yaml.FullLoader)
    return tasks_yaml
