import click
from dsloader.cli.download_case import download_smartds


@click.group()
def cli():
    pass


cli.add_command(download_smartds)
