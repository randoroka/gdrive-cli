import google.auth
import click
import os 
import requests
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from gdrive_cli.auth import SCOPES, login 
from gdrive_cli.utils import get_mime_type, list_files, list_dirs

#allows a user to list all contents of their drive or specify by file type like pdf or png
#can take an arguement for user to specify file type 
@click.command('list', short_help='list what user specifies in their drive')
@click.argument('filter', required=False, default=None)
def list(filter):

    if filter not in [None, "all"]:
        click.echo(click.style("Error:", bold=True) + " Argument not recognized")
        return

    if filter is None:
        query = "'root' in parents"
    elif filter == "all":
        query = ""

    try:
        files = list_files(query)
        if files:
            for file in files:
                click.echo(f'{file.get("name")}, {file.get("id")}')
        else:
            click.echo(click.style("Error:", bold=True) + " No files found")
    except RuntimeError as error:
        click.echo(click.style("Error:", bold=True) + f" {error}")
    except Exception as e:
        click.echo(click.style("Error:", bold=True) + f"{e}")



#lists directories on drives
# lists only root directories by default, but can list all directories including subfolders if specified using all
@click.command('list-dir', short_help='List directories in Google Drive')
@click.argument('filter', required=False, default=None)
def list_dir(filter):
  
    #specifies query to pass into list_dir function
    if filter == "all":
        query = "mimeType='application/vnd.google-apps.folder'"
    if filter is None:#the default, if arguement all is not given, only lists root folders and not subfolders
        query = "mimeType='application/vnd.google-apps.folder' and 'root' in parents"
    
    try:
        directories = list_dirs(query)
        if directories:
            for directory in directories:
                click.echo(f'{directory.get("name")}, {directory.get("id")}')
        else:
            click.echo(click.style("Error: ", bold=True) + " No files found")
    except RuntimeError as error:
        click.echo(click.style("Error: ", bold=True) + f" {error}")
    except Exception as e:
        click.echo(click.style("Error: ", bold=True) + f"{e}")






if __name__ == "__main__":
  list()