import click 
import io
import os
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.credentials import Credentials


#TO DO download by name also, not just id. may have to create func in utils that converts id to name and returns name
# only downloads folders 
@click.command('pull', short_help='list what user specifies in their drive')
@click.argument('filter', required=False, default=None)
def download_file(filter):
  
  creds = Credentials.from_authorized_user_file("../token.json")

  try:
    # create drive api client
    service = build("drive", "v3", credentials=creds)

    file_id = filter

    # may need converting id to name logic elsewhere in code. maybe add a func to utils for it??
    file_metadata = service.files().get(fileId=file_id, fields='id, name, mimeType').execute()
    folder_name = file_metadata['name']
    mimeType = file_metadata['mimeType']

    #to download a folder
    if mimeType == "application/vnd.google-apps.folder":
      
      query = f"'{file_id}' in parents"
      results = service.files().list(q=query, fields="files(id, name)").execute()
      items = results.get('files', [])
      if not items:
            click.echo(click.style("Error:", bold=True) + "No files found in the folder.")
            return

            # Download each file in the folder
      os.makedirs(folder_name)
      for item in items:
         file_id = item['id']
         file_name = item['name']
         file_path = os.path.join(folder_name, file_name)
         click.echo(f"Downloading file: {file_name}")

         request = service.files().get_media(fileId=file_id)
         fh = io.BytesIO()
         downloader = MediaIoBaseDownload(fh, request)
         done = False
         while done is False:
                status, done = downloader.next_chunk()
                click.echo(f"Download {int(status.progress() * 100)}%.")
        # Write the file to disk
         with open(file_path, 'wb') as f:
            f.write(fh.getvalue())
         click.echo(f"File downloaded as: {file_name}")
      return

  except HttpError as error:
    click.echo(click.style("Error:", bold=True) + f"{error}")
    file = None
  except Exception as e:
     click.echo(click.style("Error: ", bold=True) + f"{e}")
    