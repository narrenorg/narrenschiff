import sys
import subprocess
from abc import ABC
from abc import abstractmethod

import click

from narrenschiff.log import NarrenschiffLogger


logger = NarrenschiffLogger()


class NarrenschiffModuleException(Exception):
    """Use when something goes wrong in modules."""

    pass


class NarrenschiffModule(ABC):
    """
    Abstract class/Interface for the module classes. A module must inherit
    from this class.
    """

    def __init__(self, command):
        """
        Construct a module that executes command.

        :param command: Arguments for the module used to construct a command
        :type command: ``str``, ``int``, ``list``, or ``dict``
        :return: Void
        :rtype: ``None``
        """
        self.command = command

    def __str__(self):
        return self.__class__.__name__.lower()

    def __repr__(self):
        module = self.__class__.__module__
        name = self.__class__.__name__
        return '<{}.{} object at {}>'.format(module, name, hex(id(self)))

    def execute(self):
        """Parse command and its arguments, and execute the module."""
        output, rc = self.subprocess(self.cmd)
        self.echo(output, rc)

    @property
    @abstractmethod
    def cmd(self):
        """
        Get command that module needs to execute later.

        :return: Full command with all parameters
        :rtype: ``str``
        """
        pass

    def subprocess(self, cmd):
        """
        Execute command with shell, and return output and return code.

        :param cmd: Command to execute
        :type cmd: ``str``
        :return: output and return code
        :rtype: ``tuple``

        Example::

            output, rc = self.subprocess('kubectl get pods')
        """
        process = subprocess.run(
            cmd,
            shell=True,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        output = process.stdout if process.stdout else process.stderr

        logger.info(f'Command "{cmd}" executed')
        logger.debug(output)

        return output.decode('utf-8'), process.returncode

    def echo(self, output, rc):
        """
        Print output to console, and exit if return code is different from 0.

        :param output: stdout or stderr of a process
        :type output: ``str``
        :param rc: Return code of the process
        :type rc: ``int``
        :return: Void
        :rtype: ``None``
        """
        color = 'green' if rc == 0 else 'red'

        if output == '' and rc == 0:
            # No output from the task, but operation was successful
            output = 'Operation successfully executed!'

        click.secho(output, fg=color)

        if rc:
            sys.exit(rc)
