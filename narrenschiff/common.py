# Copyright 2021 The Narrenschiff Authors

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import re
import subprocess
from contextlib import suppress


class AmbiguousConfiguration(Exception):
    """Give warning that something is wrong with configuration."""

    pass


class Singleton(type):
    """
    Define the Singleton.
    """

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class DeleteFile:
    """Delete file from the file system, ideally in secure manner."""

    def __init__(self, path):
        """
        Make an instance of :class:`narrenschiff.common.DeleteFile` class.

        :param path: Absolute path to the file that needs to be deleted
        :type path: ``str``
        :return: Void
        :rtype: ``None``
        """
        self.path = path

    def delete(self):
        """Delete the file."""
        try:
            subprocess.run(['shred', self.path])
        except Exception:
            self._placebo_delete(passes=3)

        os.remove(self.path)

    def _placebo_delete(self, passes=1):
        """
        Overwrite file before deletaion. This is executed in case the OS
        does not have the ``shred`` command line utility. This may not work for
        modern systems that use journaling file systems, copy-on-write file
        systems, wear leveling, or similar.

        :param passes: Number of times file will be overwritten
        :type passes: ``int``
        :return: Void
        :rtype: ``None``
        """
        length = os.path.getsize(self.path)
        with open(self.path, 'wb') as f:
            for _ in range(passes):
                f.seek(0)
                f.write(os.urandom(length))
                os.fsync(f)


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


def is_jinja(filename):
    return bool(re.search(r'j(inja)?2$', filename, re.I))
