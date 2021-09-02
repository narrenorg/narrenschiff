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

import re
import time
import subprocess

import click

from narrenschiff.modules.common import NarrenschiffModule
from narrenschiff.modules.common import NarrenschiffModuleException


class WaitForPod(NarrenschiffModule):
    """Use this module when you need to wait for a pod to become ready."""

    def execute(self):
        timeout = 300  # 5min
        pod_name = self.command['grep_pod_name']
        start_time = time.time()

        while True:
            process = subprocess.run(
                self.cmd,
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            output = process.stdout.decode('utf-8')

            # output, rc = self.subprocess(cmd)
            # if rc: -> sys.exit (something went wrong) print(output)

            r = re.search(r'^{}.*\s+(\d)/\d.*'.format(pod_name), output, re.M)
            if int(r.group(1)) == self.command['threshold_replicas']:
                click.secho('Pod ready', fg='green')
                # self.echo('Pod ready', rc)
                break

            if time.time() - start_time >= timeout:
                raise NarrenschiffModuleException('Timeout exceeded')

            # click.secho('Waiting...', fg='green')
            time.sleep(1)

    @property
    def cmd(self):
        namespace = self.command['namespace']
        return 'kubectl get pods --namespace {}'.format(namespace)

    def dry_run_supported(self, cmd):
        return False
