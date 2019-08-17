from narrenschiff.modules.common import NarrenschiffModule


class Kubectl(NarrenschiffModule):

    def __init__(self, command):
        self.command = command
