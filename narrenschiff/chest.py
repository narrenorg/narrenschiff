import os
import yaml


class ChestException(Exception):
    """Use when anything goes wrong with encryption process."""

    pass


class Keychain:
    """Bundle password and salt."""

    def __init__(self):
        conf = self.load_configuration_file()
        self.key = self.load_value(conf.get('key'))
        self.spice = self.load_value(conf.get('spice'))

    def load_value(self, path):
        """
        Load value from file on the given path.

        :param path: Path to the file
        :type path: ``str``
        """
        with open(path, 'r') as f:
            secret = f.readlines()[0]
        return secret.rstrip()

    def load_configuration_file(self):
        """
        Load ``.narrenschiff.yaml`` configuration file.
        """
        path = self.get_configuration_path()
        with open(path, 'r') as f:
            conf = yaml.load(f, Loader=yaml.FullLoader)
        return conf

    def get_configuration_path(self):
        """
        Get path to the existing configuration file.

        :return: Path to configuraiton file
        :rtype: ``str``
        """
        project = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(project, os.pardir))
        narrenschiff = os.path.join(project_root, '.narrenschiff')

        path = ''

        narrenschiff_yaml = '.'.join([narrenschiff, 'yaml'])
        narrenschiff_yml = '.'.join([narrenschiff, 'yml'])

        conf_yaml = self.check_configuration_file_exists(narrenschiff_yaml)
        conf_yml = self.check_configuration_file_exists(narrenschiff_yml)

        if bool(conf_yaml) != bool(conf_yml):
            return conf_yaml or conf_yml

        exception = 'Ambiguous configuration. Either missing or duplicated'
        raise ChestException(exception)

    def check_configuration_file_exists(self, path):
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


class AES256Cypher:
    """Encode and/or decode strings."""

    def __init__(self, password, salt):
        self.password = password
        self.salt = salt
        self.key = None

    def encrypt(self):
        pass

    def decrypt(self):
        pass


class Chest:
    """Manipulate chest file."""

    pass
