import os
import click
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseUpload
from gdrive_cli.utils import resumable, create_folder, get_mime_type

# uploads files or directories with their files to drive
@click.command('push', short_help='Uploads files to Google Drive')
@click.argument('file_path', required=False, default=None)
def upload(file_path):

    creds = Credentials.from_authorized_user_file("../token.json")


    if file_path is None:
        click.echo(click.style("Error: ", bold=True) + "No file path provided")
        return
    
    if not os.path.exists(file_path):
        click.echo(click.style("Error: ", bold=True) + "Incorrect path")
        return
    
    
    if os.path.isfile(file_path):
        
        _, extension = os.path.splitext(file_path)
        mimeType = get_mime_type(extension)
        file_metadata = {'name': os.path.basename(file_path)}
        file_size = os.path.getsize(file_path)
    

        if file_size <= 5 * 1024 * 1024:
            try:
                service = build('drive', 'v3', credentials=creds)
                media = MediaFileUpload(file_path, mimetype=mimeType, resumable=False) #sets mimetype
                file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            except HttpError as error:
                click.echo(click.style("Error:", bold=True) + f" {error}")
            except Exception as e:
                click.echo(click.style("Error:", bold=True) + f"{e}")
                
            return

        #uses resumable upload if file is greater than 5 mb
        try:
            resumable(file_path, file_metadata, None)
        except RuntimeError as error:
            click.echo(click.style("Error:", bold=True) + f" {error}")
        except Exception as e:
            click.echo(click.style("Error:", bold=True) + f"{e}")
            
        return
    
    #uploads folders and their directories 
    if os.path.isdir(file_path):
        folder_metadata = {'name': os.path.basename(file_path), 'mimeType': 'application/vnd.google-apps.folder'}
        folder_id = create_folder(folder_metadata)

        for filename in os.listdir(file_path):
            full_path = os.path.join(file_path, filename)
            if os.path.isfile(full_path):
                file_metadata = {'name': os.path.basename(full_path), 'parents': [folder_id]}
                try:
                    resumable(file_path, file_metadata, None)
                except RuntimeError as error:
                    click.echo(click.style("Error:", bold=True) + f" {error}")
                except Exception as e:
                    click.echo(click.style("Error:", bold=True) + f"{e}")

        
