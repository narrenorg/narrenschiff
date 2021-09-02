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

from narrenschiff.autocomplete import ShellAutocomplete


@click.group()
def autocomplete():
    """
    Manage autocomplete script for your environment.
    \f

    :return: Void
    :rtype: ``None``
    """
    pass


@autocomplete.command()
@click.option('--shell',
              required=False,
              default='bash',
              show_default=True,
              type=str,
              help='Type of the shell.')
def add(shell):
    """
    Add autocomplete script to your environment.
    \f

    :param shell: Type of the shell you are using
    :type shell: ``str``
    :return: Void
    :rtype: ``None``
    """
    autocomplete = ShellAutocomplete()
    autocomplete.add()
