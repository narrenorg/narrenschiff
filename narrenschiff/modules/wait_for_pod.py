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
        cmd = self.get_cmd()
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
