import logging
import logging.config

from narrenschiff.common import Singleton


LOGGING = {
    'version': 1,
    'handlers': {
        'null': {
            'class':'logging.NullHandler',
        },
    },
    'loggers': {
        'narrenschiff': {
            'handlers':['null'],
            'propagate': True,
            'level':'INFO',
        },
    }
}

logging.config.dictConfig(LOGGING)


class NarrenschiffLogger(metaclass=Singleton):

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
        formatter = logging.Formatter('%(levelname)s %(asctime)s %(message)s')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(NarrenschiffLogger.LOG_LEVEL.get(verbosity))

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)
