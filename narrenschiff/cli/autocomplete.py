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
