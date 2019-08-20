from narrenschiff.modules.common import NarrenschiffModule
import subprocess


class Gcloud(NarrenschiffModule):
    """``GCloud`` module."""

    gcloud_cmd = 'gcloud'

    def execute(self):
        command = self.command.get('command')

        cmd = ' '.join([Gcloud.gcloud_cmd, command])
        subprocess.check_call(cmd, shell=True)
