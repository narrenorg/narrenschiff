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

    def __init__(self, tasks):
        """
        Construct a :class:`narrenschiff.task.TasksEngine` class.

        :param tasks: List of tasks
        :type tasks: ``list`` of :class:`narrenschiff.task.Task`
        :param template: Template environment of the course project
        :type template: :class:`narrenschiff.templating.Template`
        :return: Void
        :rtype: ``None``
        """
        self.tasks = tasks
        self.width = int(subprocess.check_output(['tput', 'cols']).decode())

    def run(self):
        """
        Start executing tasks.

        :return: Void
        :rtype: ``None``
        """
        print()
        try:
            for task in self.tasks:
                width = int(self.width) - 41 - len(task.name)
                current_time = datetime.datetime.now()
                fill = '*' * width
                print('* [', current_time, '] * [', task.name, ']', fill, '\n')
                task.command.execute()
                print()
        except subprocess.CalledProcessError as e:  # noqa
            click.secho(e, fg='red')
            warning = 'Task encountered an error! Exiting...'
            click.secho(warning, fg='red', err=True)
