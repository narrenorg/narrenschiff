class AmbiguousOptions(Exception):
    """
    Use when tasks have undefined YAML tags.
    """

    pass


class Task:

    def __init__(self, task):
        self.name = task.pop('name', None)

        if len(task) > 1:
            options = ', '.join(task.keys())
            raise AmbiguousOptions('Check tags for unknown options:', options)

        # The remaining YAML tag should be command
        command_name = list(task.keys())[0]
        command_args = task.pop(command_name)
        Command = self._dynamic_module_import(command_name)
        self.command = Command(command_args)

    def __str__(self):
        return self.name

    def __repr__(self):
        module = self.__class__.__module__
        name = self.__class__.__name__
        return '<{}.{} ({})>'.format(module, name, self.name)

    def _dynamic_module_import(self, module):
        """
        Import class corresponding to YAML tag.

        :param module: Name of the command
        :type module: ``str``
        :return: Class representing the command
        :rtype: ``class``

        **Important:** A *module* in this context means the "`narrenschiff`"
        module. This is a module that deals with executing the command
        described in ``tasks.yaml`` file i.e. the "`course`" file.
        """
        path = 'narrenschiff.modules.{}'.format(module.lower())
        klass = module.capitalize()
        mod = __import__(path, fromlist=[klass])
        return getattr(mod, klass)
