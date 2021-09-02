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

import narrenschiff
from narrenschiff.cli.env import env
from narrenschiff.cli.lint import lint
from narrenschiff.cli.dock import dock
from narrenschiff.cli.sail import sail
from narrenschiff.cli.chest import chest
from narrenschiff.cli.secretmap import secretmap
from narrenschiff.cli.autocomplete import autocomplete
from narrenschiff.log import NarrenschiffLogger


@click.group()
@click.option('--verbosity',
              'verbosity',
              required=False,
              type=int,
              help='Set verbosity (levels available are from 1 to 5)')
@click.version_option(narrenschiff.__version__, message='%(version)s')
def narrenschiff(verbosity=0):
    """
    Base command.
    \f

    :return: Void
    :rtype: ``None``
    """
    logger = NarrenschiffLogger()
    logger.set_verbosity(verbosity)


narrenschiff.add_command(env)
narrenschiff.add_command(lint)
narrenschiff.add_command(dock)
narrenschiff.add_command(sail)
narrenschiff.add_command(chest)
narrenschiff.add_command(secretmap)
narrenschiff.add_command(autocomplete)
