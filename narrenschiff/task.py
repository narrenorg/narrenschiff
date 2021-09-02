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

import subprocess
import datetime
import click


class AmbiguousOptions(Exception):
    """Use when tasks have undefined YAML tags."""

    pass


class Task:
    """
    Parse the smallest unit of the course.

    Each dictionary item from the task list should be wrapped with this class::

        course = [{'name': 'Kustomize', 'kustomization': 'examples/app/'}]
        tasks = [Task(t) for t in course]

        task = tasks[0]
        task.name  # --> 'Kustomize'
        taks.kustomization  # --> instance of Kustomization class
    """

    def __init__(self, task):
        self.name = task.pop('name', None)
        self.beacons = set(task.pop('beacons', []))

        if len(task) > 1:
            options = ', '.join(task.keys())
            raise AmbiguousOptions('Check tags for unknown options:', options)

        # The remaining YAML tag should be command
        command_name = list(task.keys())[0]
        command_args = task.pop(command_name)
        Command = self._dynamic_module_import(command_name)
        self.command = Command(command_args)

    def __str__(self):
        return self.name

    def __repr__(self):
        module = self.__class__.__module__
        name = self.__class__.__name__
        return '<{}.{} ({})>'.format(module, name, self.name)

    def _dynamic_module_import(self, module):
        """
        Import class corresponding to YAML tag.

        :param module: Name of the command
        :type module: ``str``
        :return: Class representing the command
        :rtype: ``class``

        **Important:** A *module* in this context means the "`narrenschiff`"
        module. This is a module that deals with executing the command
        described in ``tasks.yaml`` file i.e. the "`course`" file.
        """
        path = 'narrenschiff.modules.{}'.format(module.lower())
        klass = ''.join(
            '{}{}'.format(s[0].capitalize(), s[1:]) for s in module.split('_')
        )
        mod = __import__(path, fromlist=[klass])
        return getattr(mod, klass)


class TasksEngine:
    """Run course."""

    def __init__(self, tasks, beacons, dry_run_enabled):
        """
        Construct a :class:`narrenschiff.task.TasksEngine` class.

        :param tasks: List of tasks
        :type tasks: ``list`` of :class:`narrenschiff.task.Task`
        :param beacons: List of tags used to determine which task is run
        :type beacons: ``set``
        :param dry_run_enabled: Boolean indicating whether user turned on dry
            run for the task
        :type dry_run_enabled: ``bool``
        :return: Void
        :rtype: ``None``
        """
        self.tasks = tasks
        self.beacons = beacons
        self.dry_run_enabled = dry_run_enabled
        self.width = int(subprocess.check_output(['tput', 'cols']).decode())

    def run(self):
        """
        Start executing tasks.

        :return: Void
        :rtype: ``None``
        """
        click.echo()
        for task in self.tasks:
            if self.beacons:
                if self.beacons & task.beacons or 'always' in task.beacons:
                    self._execute(task)
            else:
                self._execute(task)

    def _execute(self, task):
        """
        Execute a task.

        :param task: Task that is about to get executed
        :type task: :class:`narrenschiff.task.Task`
        :return: Void
        :rtype: ``None``
        """
        width = int(self.width) - 41 - len(task.name)
        current_time = datetime.datetime.now()
        fill = '*' * width
        click.echo(
            '* [ {} ] * [ {} ] {}\n'.format(current_time, task.name, fill)
        )
        task.command.execute(dry_run_enabled=self.dry_run_enabled)
