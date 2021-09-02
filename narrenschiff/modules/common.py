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

    :cvar DRY_RUN_FLAG: ``int``

    The subprocess module does not have a way of indicating whether a command
    was run with dry run or not, since that is the responsibility of
    :meth:`narrenschiff.modules.common.NarrenschiffModule.execute` method. If
    module or subcommand of module is not supporting dry run, than
    ``DRY_RUN_FLAG`` is a reserved return code (rc) that indicates that program
    should not exit, and output should be printed in special color (blue).
    """

    DRY_RUN_FLAG = -99999

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

    def execute(self, dry_run_enabled=False):
        """
        Parse command and its arguments, and execute the module.

        :param dry_run_enabled: Boolean indicating whether user turned on dry
            run for the task
        :type dry_run_enabled: ``bool``
        :return: Void
        :rtype: ``None``
        """
        if dry_run_enabled:
            if self.dry_run_supported(self.cmd):
                output, rc = self.subprocess(f'{self.cmd} {self.dry_run}')
            else:
                output, rc = (
                    'Dry run not supported by the module or a subcommand\n',
                    NarrenschiffModule.DRY_RUN_FLAG
                )
        else:
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
        raise NotImplementedError

    @property
    def dry_run(self):
        """
        Return a dry run flag.

        :return: ``--dry-run`` string
        :rtype: ``str``

        In general most commands use ``--dry-run`` so there is no need to
        override this. However, there are exceptions for some commands where
        this flag is differently named. This property offers extensibility to
        the modules that may use different flag.
        """
        return '--dry-run'

    @abstractmethod
    def dry_run_supported(self, cmd):
        """
        Check if command supports --dry-run.

        :param cmd: Command that module should execute
        :type cmd: ``str``
        :return: Boolean indicating whether command supports dry run
        :rtype: ``bool``
        """
        raise NotImplementedError

    def subprocess(self, cmd):
        """
        Execute command with shell, and return output and return code.

        :param cmd: Command to execute
        :type cmd: ``str``
        :return: Output and return code
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

        output = process.stderr if process.stderr else process.stdout

        logger.info(f'Command "{cmd}" executed')

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
        color = self._color(rc)

        if output == '' and rc == 0:
            # No output from the task, but operation was successful
            output = 'Operation successfully executed!'

        click.secho(output, fg=color)

        if rc and rc != NarrenschiffModule.DRY_RUN_FLAG:
            sys.exit(rc)

    def _color(self, rc):
        """
        Get color for the command output.

        :param rc: Return code of the command
        :type rc: ``int``
        :return: String indicating color
        :rtype: ``str``
        """
        if rc == 0:
            return 'green'
        elif rc == NarrenschiffModule.DRY_RUN_FLAG:
            return 'blue'
        else:
            return 'red'
