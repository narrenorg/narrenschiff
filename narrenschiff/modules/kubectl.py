from narrenschiff.modules.common import NarrenschiffModule


class Kubectl(NarrenschiffModule):
    """``kubectl`` module."""

    def __init__(self, command):
        self.command = command
