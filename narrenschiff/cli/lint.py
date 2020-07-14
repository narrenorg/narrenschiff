import click
from jinja2 import Environment
from jinja2.exceptions import TemplateSyntaxError

import os

from narrenschiff.common import is_yaml
from narrenschiff.common import is_jinja


def _get_all_files(path):
    """
    Get all YAML files.

    :param path: Path to course project directory
    :type path: ``str``
    :return: List of valid narrenschiff files
    :rtype: ``list`` of ``str``

    Valid files can have following extensions: ``.yaml``, ``.yml``, ``.j2``,
    or ``.jinja2``.
    """
    paths = []
    for root, subdir, files in os.walk(path):
        for file in files:
            if is_yaml(file) or is_jinja(file):
                paths.append(os.path.join(root, file))
    return paths


def _validate_template(path):
    """
    Validate jinja template.

    :param path: Path to course project directory
    :type path: ``str``
    :return: List of valid narrenschiff files
    :rtype: ``list`` of ``str``
    """
    env = Environment()

    try:
        with open(path) as f:
            env.parse(f.read())
    except TemplateSyntaxError as e:
        click.echo(f'\033[35m{path}\033[0m: {e}')
        return 1
    return 0


@click.command()
@click.option('--location', help='Path to the directory.')
@click.pass_context
def lint(ctx, location):
    """
    Lint project files. Check if they are valid Jinja2 templates.
    \f

    :param location: Location of the secretmap file
    :type location: ``str``
    :return: Void
    :rtype: ``None``
    """
    results = []
    for file in _get_all_files(os.path.abspath(location)):
        results.append(_validate_template(file))
    ctx.exit(code=int(any(results)))
