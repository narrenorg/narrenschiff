import os

import re
import yaml

from jinja2 import Environment
from jinja2 import FileSystemLoader

from narrenschiff.chest import Keychain
from narrenschiff.chest import AES256Cipher


class TemplateException(Exception):
    """Use for exceptions regarding template manipulation."""
    pass


class VarsFileNotFoudError(Exception):
    pass


class Vars:

    def __init__(self, name, template_directory):
        """
        Initialize Var objects

        :param name: ``str`` name used for file search 
        """
        self.name = name
        self.template_directory = template_directory

    def _find_var_files(self):
        """
        Find all files containing variables for the templates.

        :return: List of paths to var files.
        :rtype: ``list`` of ``str``
        """
        paths = []

        has_dir = False
        has_file = False

        # Find name.yaml or name.yml file
        # yaml has presendance
        for ext in ['yaml', 'yml']:
            file_path = os.path.join(self.template_directory, "{}.{}".format(self.name, ext))
            if os.path.isfile(file_path):
                has_file = True
                break

        # Find name directory
        if os.path.isdir(self.name):
            paths.extend(self._walk_directory(file_path))
            has_dir = True

        if has_file:
            paths.append(file_path)

        if not has_file or has_dir:
            raise VarsFileNotFoundError

        return paths

    def _walk_directory(self, directory):
        """
        Walk the directory.

        :param directory: Absolute path to the directory
        :type directory: ``str``
        :return: List of files
        :rtype: ``list`` of ``str``
        """
        paths = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if re.search(r'ya?ml$', file, re.I):
                    paths.append(os.path.join(root, file))
        return paths

    def _load_vars(self, filepaths):
        """
        Load content of var files into a list.

        :param filepaths: List of file paths of var files
        :type filepaths: ``list`` of ``str``
        :return: List of dictionary values
        :rtype: ``list`` of ``dict``

        **Important:** Empty files return ``None``. This method filters out
        those values.
        """
        vars = []
        for filepath in filepaths:
            with open(filepath, 'r') as f:
                vars.append(yaml.load(f, Loader=yaml.FullLoader))
        return [var for var in vars if var]

    def load_vars(self):
        """
        Load variables.

        :return: Variables to be used for template rendering
        :rtype: ``dict``
        """
        var_files = self._find_var_files()
        plain_vars = self._load_vars(var_files)

        return plain_vars


class PlainVars(Vars):

    NAME = 'vars'

    def __init__(self, template_directory):
        super().__init__(name=PlainVars.NAME, template_directory=template_directory)


class ChestVars(Vars):

    NAME = 'chest'

    def __init__(self, template_directory):
        super().__init__(name=ChestVars.NAME, template_directory=template_directory)

    def load_vars(self):
        var_files = self._find_var_files()
        ciphertext_vars = self._load_vars(var_files)

        keychain = Keychain()
        cipher = AES256Cipher(keychain)
        for var in ciphertext_vars:
            for key, val in var.items():
                var[key] = cipher.decrypt(val)

        return ciphertext_vars


class SecretmapVars(Vars):

    NAME = 'secretmap'

    def __init__(self, template_directory):
        super().__init__(name=SecretmapVars.NAME, template_directory=template_directory)


class Template:
    """Load and manipulate templates and template environemtn."""

    def __init__(self, path):
        """
        Prepare Jinja2 templating environment.

        :param path: Path of the ``tasks.yaml`` file
        :type path: ``str``
        :return: Void
        :rtype: ``None``

        Directory containing the ``course`` (e.g. ``tasks.yaml``) file will
        be the directory from where the templates are taken to be rendered.
        """
        if not (path.endswith('.yml') or path.endswith('.yaml')):
            exception = 'Files must end with ".yaml" or ".yml" extension'
            raise TemplateException(exception)

        self.tasks_file = os.path.abspath(path)
        self.template_directory = os.path.abspath(os.path.dirname(path))

        loader = FileSystemLoader(self.template_directory)
        self.env = Environment(loader=loader)

        self.vars = {}

    def render(self, path):
        """
        Render template on the given path.

        :param path: Path to the template file
        :type path: ``str``
        :return: Rendered template
        :rtype: ``str``
        """
        template = self.env.get_template(path)
        return template.render(**self.load_vars())

    def load_vars(self):
        """
        Load variables.

        :return: Variables to be used for template rendering
        :rtype: ``dict``

        This is the order in which files containing variables are loaded:

        1. Load ``vars.yaml`` if it exists
        2. Load all files from the ``vars/`` directory if it exists
        3. Load and decrypt all variables from ``chest.yaml``
        4. Load all files from the ``chest/`` directory if it exists
        5. Merge all files

        **Important:** Files must not contain duplicate values!
        """

        vars = [
            *PlainVars(self.template_directory).load_vars(),
            *ChestVars(self.template_directory).load_vars(),
            *SecretmapVars(self.template_directory).load_vars(),
        ]

        vars_temp = []
        for var in vars:
            vars_temp.extend(list(var.keys()))

        duplicates = self.find_duplicates(vars_temp)
        if duplicates:
            exception = 'Duplicate variable names for these variables: "{}"'
            raise TemplateException(exception.format(', '.join(duplicates)))

        variables = {}
        for dct in vars:
            variables.update(dct)

        return variables

    def find_duplicates(self, values):
        """
        Find duplicate keys.

        :param values: List of keys from var and chest files.
        :type values: ``list`` of ``str``
        :return: List of duplicates
        :rtype: ``list`` of ``str``
        """
        seen = set()
        duplicates = []
        for val in values:
            if val not in seen:
                seen.add(val)
            else:
                duplicates.append(val)
        return duplicates
