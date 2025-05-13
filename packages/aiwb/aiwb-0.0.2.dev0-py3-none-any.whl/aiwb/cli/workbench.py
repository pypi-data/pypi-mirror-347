import os
import click

from aiwb.core.session import Session

@click.group(help="aiwb cli workbench subcommand")
@click.pass_obj
def cli(session):
    pass

@cli.command()
@click.pass_obj
def list(session):
    print(session.client("workbench").list())