import google.auth
import click
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from gdrive_cli.utils import get_mime_type, list_files, list_dirs, find_id


#searches google drive by file/diretory name, file/directory id, and extension 
@click.command('search', short_help='search by name, extension, or id')
@click.option('--name', type=str, help='Name of the file to search for')
@click.option('--ext', type=str, help='Extension of the file to search for')
@click.option('--id', type=str, help='ID of the file to search for')
def search(id, name, ext):

    if not (id or name or ext):
        click.echo(click.style("Error: ", bold=True) + "You must specify at least one of --id, --name, or --ext")
        return 

    if id:

        item = find_id(id)
        if item["error_message"]:
            click.echo(f"Error: {item['error_message']}")
            return

        click.echo(item["file"]["name"])

    if name:
        query = f"name='{name}'"
        items = list_files(query)
        if not items:
            click.echo(click.style("Error: ", bold=True) + "Nothing found matching name")
            return
            
        for item in items:
            click.echo(f'{item.get("name")}, {item.get("id")}')


    if ext:
        mime = get_mime_type(ext)
        if ext is not None and mime is None:
            click.echo(click.style("Error: ", bold=True) + "Extension type not recognized")
            return
        query = f"mimeType='{mime}'"
        items = list_files(query)
        if items:
            for item in items:
                click.echo(f'{item.get("name")}, {item.get("id")}')
        else:
            click.echo(click.style("Error: ", bold=True) + "Nothing with that extension type found in drive.")
    



 
    