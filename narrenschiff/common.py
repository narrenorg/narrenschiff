import os


class AmbiguousConfiguration(Exception):
    """Warn that something is wrong with configuration."""

    pass


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
