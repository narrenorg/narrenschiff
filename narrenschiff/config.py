import os
import sys
import yaml
import click


class ConfigurationException(Exception):
    """Use when something goes wrong with the configuration."""

    pass


class NarrenschiffConfiguration:
    """
    Load configuration file.

    This class should never be called directly, nor it should be inherited
    from. Other classes should use it by composition principle (see
    implementation of e.g. :class:`narrenschiff.config.Keychain`). This should
    make classes, that depend on subset of config, easier to test.
    """

    def __init__(self):
        conf = self._load_configuration_file()

        self.key = self._load_value(conf.get('key'))
        self.spice = self._load_value(conf.get('spice'))

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
            conf = yaml.load(f, Loader=yaml.FullLoader)
        return conf

    def _get_configuration_path(self):
        """
        Get path to the existing configuration file.

        :return: Path to configuraiton file
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
        Check if configuraiton file exists. If it exists, return its path.

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
        configuraiton = NarrenschiffConfiguration()

        self.key = configuraiton.key
        self.spice = configuraiton.spice
