import os
import io
import json
import click
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseUpload
from utils import resumable, create_folder

# uploads files or directories with their files to drive
@click.command('push', short_help='Uploads files to Google Drive')
@click.argument('file_path', required=False, default=None)
def upload(file_path):

    creds = Credentials.from_authorized_user_file("../token.json")


    if not os.path.exists(file_path):
        click.echo("Incorrect path")
        return 
    
    
    if os.path.isfile(file_path):
        file_metadata = {'name': os.path.basename(file_path)}
        file_size = os.path.getsize(file_path)
        if file_size <= 5 * 1024 * 1024:
            print("under5")
            service = build('drive', 'v3', credentials=creds)
            media = MediaFileUpload(file_path, resumable=True)
            file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            return

        resumable(file_path, file_metadata, None)
        return
    
    #uploads folders and their directories 
    if os.path.isdir(file_path):
        folder_metadata = {'name': os.path.basename(file_path), 'mimeType': 'application/vnd.google-apps.folder'}
        folder_id = create_folder(folder_metadata)

        for filename in os.listdir(file_path):
            full_path = os.path.join(file_path, filename)
            if os.path.isfile(full_path):
                print(full_path)
                file_metadata = {'name': os.path.basename(full_path), 'parents': [folder_id]}
                resumable(full_path, file_metadata, folder_id)

upload("/Users/Ariel/Desktop/UploadingPractoce")
        

 

  