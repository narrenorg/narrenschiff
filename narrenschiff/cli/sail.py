# Copyright 2021 The Narrenschiff Authors

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import click
import yaml

from narrenschiff.task import Task
from narrenschiff.task import TasksEngine
from narrenschiff.templating import Template
from narrenschiff.config import Keychain
from narrenschiff.config import KubectlContext
from narrenschiff.secretmap import Secretmap


@click.command()
@click.option('--set-course', 'course', help='Path to your YAML course file.')
@click.option(
    '--follow-beacons',
    'beacons',
    required=False,
    type=str,
    help='Execute tasks marked only by given beacons (comma separated list).')
@click.option('--dry-run', required=False, is_flag=True)
def sail(course, beacons, dry_run):
    """
    Turn tasks into actions.
    \f

    :param course: The path to ``course`` file. A file containing tasks
        specified in the YAML format. Tasks are ``executable`` pieces of
        configuration. Course is Jinja2 templated file (as are all the
        kubernetes manifest files)
    :type course: ``str``
    :return: Void
    :rtype: ``None``
    """
    context = KubectlContext()

    template = Template()
    template.set_course(course)

    secretmap = Secretmap(Keychain(), os.path.dirname(course))

    tasks = _import_course(os.path.basename(course), template)

    template.render_all_files()
    secretmap.render_all_files()

    try:
        beacons = set(beacons.split(','))
    except AttributeError:
        beacons = set()

    engine = TasksEngine(tasks, beacons, dry_run)

    try:
        _check_or_switch(context)
        engine.run()
    finally:
        _check_or_switch(context)
        template.clear_templates()
        secretmap.clear_all_files()


def _check_or_switch(context):
    """
    Change context for the kubectl command.

    :param context: Context configuration class
    :type context: :class:`narrenschiff.config.KubectlContext`
    :return: Void
    :rtype: ``None``
    """
    if context.use:
        context.switch()


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
    tasks_raw = template.render(course)
    tasks_yaml = yaml.safe_load(tasks_raw)
    return tasks_yaml
