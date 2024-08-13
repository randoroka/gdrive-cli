import click
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# deletes files and folders
@click.command('rm', short_help='deletes files')
@click.argument('file_id', required=False, default=None)
def delete_file(file_id):
    creds = Credentials.from_authorized_user_file("../token.json")
    service = build('drive', 'v3', credentials=creds)

    try:
        service.files().delete(fileId=file_id).execute()
        click.echo(f"File with ID '{file_id}' deleted.")
    except HttpError as error:
        click.echo(click.style("Error: ", bold=True) + f"An error occurred: {error}")
    except Exception as e:
        click.echo(click.style("Error: ", bold=True) + f"{e}")
        
# makes a link of folder in drive to share 
@click.command('link', short_help='deletes files')
@click.argument('folder_id', required=False, default=None)         
def shareable_link(folder_id):
    try:
        # Load credentials
        creds = Credentials.from_authorized_user_file("../token.json")
        service = build('drive', 'v3', credentials=creds)
        
        user_permission = {
            'type': 'anyone',  
            'role': 'reader'   
        }
        
        # Set the permission to the folder
        service.permissions().create(
            fileId=folder_id,
            body=user_permission,
            fields='id'
        ).execute()

        # Retrieve the shareable link
        folder = service.files().get(fileId=folder_id, fields='webViewLink').execute()
        click.echo(f"URL for the folder: {folder.get('webViewLink')}")
    
    except HttpError as error:
        # Handles errors related to the Google Drive API
        click.echo(click.style("Error: ", bold=True) + f"{error}")

    except Exception as e:
        # Handles all other exceptions
        click.echo(click.style("Error: ", bold=True) + f"{e}")