class NarrenschiffModule:
    """
    Abstract class/Interface for the module classes. A module must inherit
    from this class.
    """

    def __str__(self):
        return self.__class__.__name__.lower()

    def __repr__(self):
        module = self.__class__.__module__
        name = self.__class__.__name__
        return '<{}.{} object at {}>'.format(module, name, hex(id(self)))
