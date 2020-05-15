import unittest
import logging

from narrenschiff.log import NarrenschiffLogger


class NarrenschiffLoggerTestCase(unittest.TestCase):

    def setUp(self):
        self.logger = NarrenschiffLogger()

    def test_log_level(self):
        self.logger.set_verbosity(5)
        self.assertEqual(
            self.logger.logger.level,
            self.logger.LOG_LEVEL.get(5)
        )

    def test_wrong_log_level_does_not_change_default(self):
        self.logger.set_verbosity(0)
        self.assertEqual(
            self.logger.logger.level,
            logging.INFO
        )

    def test_narrenschiff_logger_info_translates_into_logger_jnfo_method(self):
        logger = logging.getLogger('narrenschiff')
        self.assertEqual(self.logger.info, logger.info)

    def test_getattr_returns_none_for_non_existent_attributes(self):
        self.assertEqual(None, self.logger.dummy)

    def tearDown(self):
        self.logger.logger.level = logging.INFO
