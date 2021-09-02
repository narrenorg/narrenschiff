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
import uuid
import yaml
import click


def touch(path):
    """Create a file, but don't overwrite it."""
    with open(path, 'a'):
        pass


@click.command()
@click.option('--location', help='Relative path to course project directory.')
@click.option('--autogenerate',
              required=False,
              is_flag=True,
              help='Autogenerate key and spice, and add to .narrenschiff.yaml')
def dock(location, autogenerate):
    """
    Start a project. Use autogenerate to automatically generate key and spice
    in users home directory. This is compatible only with UNIX systems. Be
    careful with this command, it can overwrite your existing configuration!
    \f

    :param location: Path to the course directory
    :type location: ``str``
    :return: Void
    :rtype: ``None``
    """
    abs_location = os.path.abspath(location)
    os.makedirs(abs_location, mode=0o755, exist_ok=True)

    touch(os.path.join(os.getcwd(), ".narrenschiff.yaml"))

    for conf in ["vars.yaml", "chest.yaml", "secretmap.yaml"]:
        touch(os.path.join(abs_location, conf))

    if autogenerate:
        key = str(uuid.uuid4())
        spice = str(uuid.uuid4())

        root_project_name = os.path.basename(os.getcwd())
        project_config_path = os.path.join(
            os.path.expanduser('~'),
            f'.{root_project_name}'
        )

        key_path = os.path.join(project_config_path, 'key.txt')
        spice_path = os.path.join(project_config_path, 'spice.txt')

        os.makedirs(project_config_path)

        with open(key_path, 'w') as f:
            f.write(key)

        with open(spice_path, 'w') as f:
            f.write(spice)

        dot_narrenschiff = {
            'key': key_path.replace(os.path.expanduser('~'), '~'),
            'spice': spice_path.replace(os.path.expanduser('~'), '~')
        }

        with open('.narrenschiff.yaml', 'w') as f:
            yaml.dump(dot_narrenschiff, f)

        click.echo(f'Credentials are located in {project_config_path}')
