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
