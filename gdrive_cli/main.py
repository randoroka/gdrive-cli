# gdrive_cli/main.py
import click
from gdrive_cli.list_content import list, list_dir, list_local
from gdrive_cli.search_content import search
from gdrive_cli.auth import login, logout
from gdrive_cli.modify_local import rename, change_all
from gdrive_cli.download import download_file
from gdrive_cli.upload import upload


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
cli.add_command(upload)



if __name__ == "__main__":
    cli()
