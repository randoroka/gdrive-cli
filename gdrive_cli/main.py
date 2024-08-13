# gdrive_cli/main.py
import click
from gdrive_cli.list_content import list, list_dir
from gdrive_cli.search_content import search
from gdrive_cli.auth import login, logout, check_login
from gdrive_cli.modify_local import rename, change_all
from gdrive_cli.download import download_file
from gdrive_cli.upload import upload
from gdrive_cli.modify_drive import delete_file


def check_login_required(ctx, command_name):
    if command_name not in ['login', 'logout']:
        check_login() #checks user is logged first in when they run any command
        
@click.group()
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand:
        check_login_required(ctx, ctx.invoked_subcommand)

cli.add_command(login)
cli.add_command(logout)
cli.add_command(list)
cli.add_command(list_dir)
cli.add_command(search)
cli.add_command(rename)
cli.add_command(change_all)
cli.add_command(download_file)
cli.add_command(upload)
cli.add_command(delete_file)



if __name__ == "__main__":
    cli()
