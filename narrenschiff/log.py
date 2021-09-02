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

import logging
import logging.config
from colorlog import ColoredFormatter

from narrenschiff.common import Singleton


LOGGING = {
    'version': 1,
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    'loggers': {
        'narrenschiff': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
    }
}

logging.config.dictConfig(LOGGING)


class NarrenschiffLogger(metaclass=Singleton):
    """Set narrenschiff log level and print to STDOUT."""

    LOG_LEVEL = {
        5: logging.DEBUG,
        4: logging.INFO,
        3: logging.WARNING,
        2: logging.ERROR,
        1: logging.CRITICAL
    }

    def __init__(self):
        self.logger = logging.getLogger('narrenschiff')

    def set_verbosity(self, verbosity):
        """
        Set verbosity of the logger.

        :param verbosity: Verbosity level
        :type verbosity: ``int``

        Verbosity can be from 1 to 5, corresponding to five log levels.
        """
        if verbosity not in range(1, 6):
            return
        formatter = ColoredFormatter(
            '%(log_color)s%(levelname)s %(asctime)s %(message)s',
            log_colors={
                'DEBUG': 'blue',
                'INFO': 'white',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bold',
            },
        )
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(NarrenschiffLogger.LOG_LEVEL.get(verbosity))

    def __getattr__(self, name):
        log_levels = ['debug', 'info', 'warning', 'error', 'critical']
        if name in log_levels:
            return getattr(self.logger, name)
