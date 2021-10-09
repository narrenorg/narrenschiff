from narrenschiff.modules.common import NarrenschiffModule


class Echo(NarrenschiffModule):

    @property
    def cmd(self):
        return f'echo "{self.command.get("command")}"'

    def dry_run_supported(self, cmd):
        return False
