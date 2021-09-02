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

import click

import os
import re
import platform
import subprocess
from shutil import which

import narrenschiff


def _check_cmd(cmd, subcommand, formatted):
    """Check if command exists on the PATH."""
    if not which(f'{cmd}'):
        click.echo(f'* {cmd}: Not found')
    else:
        click.echo(f'* {cmd}')
        if formatted:
            click.echo('```')
        subprocess.run(f'{cmd} {subcommand}', shell=True)
        if formatted:
            click.echo('```')


def _dependency_management(formatted):
    """Detect all dependency management tools."""
    tools = ['pip', 'pipenv', 'pip-compile', 'pip-sync', 'poetry']
    detected = []
    for tool in tools:
        check_tool = subprocess.run(f'{tool} --version',
                                    shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        if check_tool.returncode == 0:
            version = re.search(
                r'\d+\.\d+\.\d+',
                check_tool.stdout.decode().strip()
            ).group()
        else:
            version = 'Not Found'
        detected.append({
            'tool': tool,
            'version': version
        })

    click.echo('* Dependency management')
    if formatted:
        click.echo('\n| Dependency management tool | Version |')
        click.echo('| :------------------------: | :-----: |')

    for tool in detected:
        if formatted:
            click.echo(f'| {tool["tool"]} | {tool["version"]} |')
        else:
            click.echo(f'{tool["tool"]}: {tool["version"]}')


@click.command()
@click.option('--formatted',
              required=False,
              is_flag=True,
              help='Output in Markdown format.')
def env(formatted):
    """Show environment info."""
    click.echo(f'* narrenschiff: {narrenschiff.__version__}')
    click.echo(f'* OS: {platform.platform()}')
    _check_cmd('python', '-VV', formatted)
    _dependency_management(formatted)
    click.echo(f'* virtualenv: {"yes" if os.getenv("VIRTUAL_ENV") else "no"}')
    _check_cmd('gcloud', 'version', formatted)
    _check_cmd('kubectl', 'version', formatted)
    _check_cmd('helm', 'version', formatted)
