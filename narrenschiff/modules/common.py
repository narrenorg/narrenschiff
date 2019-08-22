from abc import ABC
from abc import abstractmethod


class NarrenschiffModuleException(Exception):
    """Use when something goes wrong in modules."""

    pass


class NarrenschiffModule(ABC):
    """
    Abstract class/Interface for the module classes. A module must inherit
    from this class.
    """

    def __init__(self, command, template):
        """
        Construct a module that executes command.

        :param command: Arguments for the module used to construct a command
        :type command: ``str``, ``int``, ``list``, or ``dict``
        :param template: Template environment of the course project
        :type template: :class:`narrenschiff.templating.Template`
        :return: Void
        :rtype: ``None``
        """
        self.command = command
        self.template = template

    def __str__(self):
        return self.__class__.__name__.lower()

    def __repr__(self):
        module = self.__class__.__module__
        name = self.__class__.__name__
        return '<{}.{} object at {}>'.format(module, name, hex(id(self)))

    @abstractmethod
    def execute(self):
        pass
