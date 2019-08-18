from narrenschiff.modules.common import NarrenschiffModule
from narrenschiff.modules.common import NarrenschiffModuleException


class Kustomization(NarrenschiffModule):
    """``kustomization`` module. Wrapper around ``kubectl apply -k dir/``."""

    def execute(self):
        if not isinstance(self.command, str):
            exception = 'This module does not support additional arguments'
            raise NarrenschiffModuleException(exception)

        cmd = 'kubectl apply -k "{}"'.format(self.command)
        print(cmd)
