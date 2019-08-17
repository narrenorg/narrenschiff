import os

import yaml

from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import select_autoescape


class TemplateException(Exception):

    pass


class Template:

    def __init__(self, path):
        """
        Prepare Jinja2 templating environment.

        :param path: Path of the ``tasks.yaml`` file
        :type path: ``str``
        :return: Void
        :rtype: ``None``

        Directory containing the ``chart`` (e.g. ``tasks.yaml``) file will
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
        3. Load and decrypt all variables from ``vault.yaml``
        4. Merge all files

        **Important:** Files must not contain duplicate values!
        """
        var_files = self.find_var_files('vars')
        vault_files = self.find_var_files('vault')

        vars = [*self._load_vars(var_files), *self._load_vars(vault_files)]

        vars_temp = []
        for var in vars:
            vars_temp.extend(list(var.keys()))

        duplicates = self.find_duplicates(vars_temp)
        if duplicates:
            exception = 'Duplicate variable names for these variables: "{}"'
            raise TemplateException(exception.format(', '.join(duplicates)))

        variables = {}
        for var in vars:
            variables.update(var)

        return variables

    def _load_vars(self, filepaths):
        """
        Load content of var files into a list.

        :param filepaths: List of file paths of var and valut files
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

    def find_var_files(self, filename):
        """
        Find all files containing variables for the templates.

        :param filename: The name of the var file (``vars`` or ``vault``)
        :type filename: ``str``
        :return: List of paths to var files.
        :rtype: ``list`` of ``str``
        """
        paths = []
        var_files = [s.format(filename) for s in ['{}.yaml', '{}.yml', '{}']]
        for file in var_files:
            file_path = '{}/{}'.format(self.template_directory, file)

            if file == 'vars' or file == 'vault':
                paths.extend(self.walk_directory(file_path))
                continue

            if os.path.exists(file_path):
                paths.append(file_path)
        return paths

    def walk_directory(self, directory):
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
                paths.append(os.path.join(root, file))
        return paths

    def find_duplicates(self, values):
        """
        Find duplicate keys.

        :param values: List of keys from var and vault files.
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
