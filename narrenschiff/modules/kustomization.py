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

from narrenschiff.modules.mixins import KubectlDryRunMixin
from narrenschiff.modules.common import NarrenschiffModule
from narrenschiff.modules.common import NarrenschiffModuleException
from narrenschiff.templating import Template
from narrenschiff.log import NarrenschiffLogger


logger = NarrenschiffLogger()


class Kustomization(KubectlDryRunMixin, NarrenschiffModule):
    """``kustomization`` module. Wrapper around ``kubectl apply -k dir/``."""

    @property
    def cmd(self):
        logger.info('Executing kustomization task')
        if not isinstance(self.command, str):
            exception = 'This module does not support additional arguments'
            raise NarrenschiffModuleException(exception)

        path = os.path.join(Template().tmp, self.command)
        logger.debug(f'Executing kustomization module on {path}')

        return f'kubectl apply -k "{path}"'
