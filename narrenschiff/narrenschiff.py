import click


@click.group()
def narrenschiff():
    pass


@narrenschiff.command()
def deploy():
    click.echo('Ahoy!')
