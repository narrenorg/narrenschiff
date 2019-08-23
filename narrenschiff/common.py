import os
from contextlib import suppress
import re


class AmbiguousConfiguration(Exception):
    """Warn that something is wrong with configuration."""

    pass


class Singleton(type):
    """
    Define an Instance operation that lets clients access its unique
    instance.
    """

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


def get_chest_file_path(location):
    """
    Check if there are duplicate chest files, and return paths if there are
    not.

    :param location: Relative path to course project directory
    :type location: ``str``
    :return: Absolute path to chest file
    :rtype: ``str``
    :raises: :class:`narrenschiff.common.AmbiguousConfiguration`
    """
    paths = ['chest.yaml', 'chest.yml']
    cwd = os.getcwd()
    candidate = []
    for path in paths:
        chest_file = os.path.join(cwd, location, path)
        if os.path.exists(chest_file):
            candidate.append(chest_file)

    candidate_length = len(candidate)
    if candidate_length > 1:
        raise AmbiguousConfiguration('Only one chest file can exist')
    if candidate_length == 0:
        raise AmbiguousConfiguration('Chest file does not exist')
    return candidate[0]


def flatten(lst):
    """
    Flatten list.

    :param lst: A list to be flattened
    :type lst: ``list``
    :return: Flattened list
    :rtype: ``list``
    """
    flattened = []
    for element in lst:
        if isinstance(element, str):
            flattened.append(element)
        else:
            with suppress(TypeError):
                flattened.extend(element)
    return flattened


def is_yaml(filename):
    return bool(re.search(r'ya?ml$', filename, re.I))
