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
import sys
import subprocess

import yaml
import click

from narrenschiff.log import NarrenschiffLogger


logger = NarrenschiffLogger()


class ConfigurationException(Exception):
    """Use this when something goes wrong with the configuration."""

    pass


class NarrenschiffConfiguration:
    """
    Load configuration file.

    This class should never be called directly, nor it should be inherited
    from. Other classes should use it by composition principle (see
    implementation of e.g. :class:`narrenschiff.config.Keychain`). This should
    make classes that depend on subset of config easier to test.
    """

    def __init__(self):
        conf = self._load_configuration_file()

        self.key = self._load_value(conf.get('key'))
        self.spice = self._load_value(conf.get('spice'))
        self.context = conf.get('context', {})

    def _load_value(self, path):
        """
        Load value from file on the given path.

        :param path: Path to the file
        :type path: ``str``
        """
        secret = ''
        try:
            with open(os.path.expanduser(path), 'r') as f:
                secret = f.readlines()[0].rstrip()
        except IndexError:
            click.secho(f'File {path} cannot be empty', fg='red')
            sys.exit(1)
        except FileNotFoundError:
            click.secho(f'File {path} not found', fg='red')
            click.secho(
                f'Please check or configure paths in {self._get_configuration_path()}',  # noqa
                fg='red'
            )
            sys.exit(1)
        return secret

    def _load_configuration_file(self):
        """
        Load ``.narrenschiff.yaml`` configuration file.
        """
        path = self._get_configuration_path()
        with open(path, 'r') as f:
            conf = yaml.safe_load(f)
        return conf

    def _get_configuration_path(self):
        """
        Get path to the existing configuration file.

        :return: Path to configuration file
        :rtype: ``str``
        """
        project_root = os.getcwd()
        narrenschiff = os.path.join(project_root, '.narrenschiff')

        narrenschiff_yaml = '.'.join([narrenschiff, 'yaml'])
        narrenschiff_yml = '.'.join([narrenschiff, 'yml'])

        conf_yaml = self._check_configuration_file_exists(narrenschiff_yaml)
        conf_yml = self._check_configuration_file_exists(narrenschiff_yml)

        if bool(conf_yaml) != bool(conf_yml):
            return conf_yaml or conf_yml

        exception = 'Ambiguous configuration. Either missing or duplicated'
        raise ConfigurationException(exception)

    def _check_configuration_file_exists(self, path):
        """
        Check if configuration file exists. If it exists, return its path.

        :param path: Path to configuration file
        :type path: ``str``
        :return: Path
        :rtype: ``str``
        """
        if os.path.isfile(path):
            return path
        return ''


class Keychain:
    """Bundle password and salt."""

    def __init__(self):
        configuration = NarrenschiffConfiguration()

        self.key = configuration.key
        self.spice = configuration.spice


class KubectlContext:
    """Handle context switching."""

    NAME = 'undefined'
    USE = 'false'

    def __init__(self):
        configuration = NarrenschiffConfiguration()

        self.name = configuration.context.get('name', KubectlContext.NAME)
        self.use = self._sanitize_boolean(
            configuration.context.get('use', KubectlContext.USE)
        )

        if self.use:
            self.old = self._get_current_context()
            self.switch_context = (self.old, self.name)

    def _sanitize_boolean(self, value):
        if isinstance(value, str):
            if value == 'true':
                return True
        if isinstance(value, bool):
            return value
        if isinstance(value, int):
            return bool(value)
        return False

    def _get_current_context(self):
        logger.info('Obtaining current kubectl context')

        process = subprocess.run(
            'kubectl config current-context',
            shell=True,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if process.returncode:
            logger.error('Could not get current context')
            logger.debug(f"{process.stderr.decode('utf-8')}")
            sys.exit(1)

        context = process.stdout.decode('utf-8').strip()
        logger.info(f'Current kubectl context is {context}')
        return context

    def switch(self):
        """Switch kubectl context."""
        old, new = self.switch_context
        logger.info(f'Switching kubectl context to {new}')

        process = subprocess.run(
            f'kubectl config use-context {new}',
            shell=True,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if process.returncode:
            logger.error('Could not switch context')
            logger.debug(f"{process.stderr.decode('utf-8')}")
            sys.exit(1)

        logger.info(f'Current kubectl context is set to {new}')
        self.switch_context = (new, old)
