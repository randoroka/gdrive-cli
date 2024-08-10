import google.auth
import click
import os 
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from auth import SCOPES, login 
from utils import get_mime_type, list_files, list_dirs

#allows a user to list all contents of their drive or specify by file type like pdf or png
#can take an arguement for user to specify file type 
@click.command('list', short_help='list what user specifies in their drive')
@click.argument('filter', required=False, default=None)
def list(filter):

    #specifies query to pass into list function
    if filter is None:
        query = "'root' in parents"

    if filter == "all":
        query = ""

    files = list_files(query)

    if not files:
        click.echo("No files found or an error occurred.")
        return
    
    if files:
        for file in files:
            click.echo(f'{file.get("name")}, {file.get("id")}')
   
    



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

    directories = list_dirs(query)

    if not directories:
        click.echo("No directories found or an error occurred.")
        return
    
    if directories:
        for directory in directories:
            click.echo(f'{directory.get("name")}, {directory.get("id")}')


#figure out why filter defaults to files in current directory and always displays that.
@click.command('ls', short_help='list what user specifies in their drive')
@click.argument('filter', required=False, default="")
def list_local(filter):

    try:
        files = os.listdir(filter)
        for file in files:
          click.echo(file)
    
    except FileNotFoundError:
        click.echo(f"Error: The specified path '{filter}' does not exist.")




if __name__ == "__main__":
  list()