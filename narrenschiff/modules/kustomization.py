import os
import click
import subprocess

from narrenschiff.modules.common import NarrenschiffModule
from narrenschiff.modules.common import NarrenschiffModuleException
from narrenschiff.templating import Template
from narrenschiff.log import NarrenschiffLogger


logger = NarrenschiffLogger()


class Kustomization(NarrenschiffModule):
    """``kustomization`` module. Wrapper around ``kubectl apply -k dir/``."""

    def execute(self):
        logger.info('Executing kustomization task')
        if not isinstance(self.command, str):
            exception = 'This module does not support additional arguments'
            raise NarrenschiffModuleException(exception)

        path = os.path.join(Template().tmp, self.command)
        cmd = 'kubectl apply -k "{}"'.format(path)

        logger.debug(f'Executing kustomization module on {path}')

        process = subprocess.run(
            cmd,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        output = process.stdout if process.stdout else process.stderr
        color = 'green' if process.stdout else 'red'

        logger.info(f'Command "{cmd}" executed')
        logger.debug(output)

        click.secho(output.decode('utf-8'), fg=color)
