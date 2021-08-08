# Copyright 2021 Petar Nikolovski

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
