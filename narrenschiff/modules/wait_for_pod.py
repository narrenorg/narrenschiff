import re
import time
import subprocess

import click

from narrenschiff.modules.common import NarrenschiffModule
from narrenschiff.modules.common import NarrenschiffModuleException


class WaitForPod(NarrenschiffModule):

    def execute(self):
        timeout = 300  # 5min
        namespace = self.command['namespace']
        pod_name = self.command['grep_pod_name']

        cmd = 'kubectl get pods --namespace {}'.format(namespace)
        start_time = time.time()

        while True:
            process = subprocess.run(
                cmd,
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            output = process.stdout.decode('utf-8')

            r = re.search(r'^{}.*\s+(\d)/\d.*'.format(pod_name), output, re.M)
            if int(r.group(1)) == self.command['threshold_replicas']:
                click.secho('Pod ready', fg='green')
                break

            if time.time() - start_time >= timeout:
                raise NarrenschiffModuleException('Timeout exceeded')

            # click.secho('Waiting...', fg='green')
            time.sleep(1)
