import click
import sys
from list_content import list, list_dir, list_local
from search_content import search
from auth import login, logout
from modify_local import rename, change_all
from download import download_file


@click.group()
def cli():
    pass

cli.add_command(login)
cli.add_command(logout)
cli.add_command(list)
cli.add_command(list_dir)
cli.add_command(search)
cli.add_command(list_local)
cli.add_command(rename)
cli.add_command(change_all)
cli.add_command(download_file)



if __name__ == "__main__":
    cli()
