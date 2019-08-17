from narrenschiff.modules.common import NarrenschiffModule


class Kustomization(NarrenschiffModule):
    """``kustomization`` module. Wrapper around ``kubectl apply -k dir/``."""

    def __init__(self, command):
        self.command = command
