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

class KubectlDryRunMixin:
    """Add dry run to kubectl related modules."""

    @property
    def dry_run(self):
        return '--dry-run=server'  # none, server, client, -o yaml

    def dry_run_supported(self, cmd):
        whitelist = [
            'run',
            'apply',
            'delete',
            'create',
            'scale',
            'autoscale',
            'patch',
            'replace',
        ]

        if cmd.split()[1] in whitelist:
            return True
        return False
