import mimetypes
import json
import os

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload, MediaIoBaseUpload

# Function to get MIME type from file extension
def get_mime_type(file_extension):
  mime_type, _ = mimetypes.guess_type(f'file.{file_extension}')
  if mime_type is None:
      mime_type = get_drive_mime(file_extension) #fixed flaw right here 
      if mime_type is None:
         return None 
      return mime_type 
  return mime_type

#gets google drive specific mime types
def get_drive_mime(file_extension):
  gdrive_mime_types = {
    'dir': 'application/vnd.google-apps.folder',
    'document': 'application/vnd.google-apps.document',
    'spreadsheet': 'application/vnd.google-apps.spreadsheet',
    'presentation': 'application/vnd.google-apps.presentation',
    'form': 'application/vnd.google-apps.form'
  }

  mime_type = gdrive_mime_types.get(file_extension)
  if mime_type:
      return mime_type
  return None 

def list_files(query):
    creds = Credentials.from_authorized_user_file("token.json")
    files = []

    try:
        # Create Drive API client
        service = build("drive", "v3", credentials=creds)
        page_token = None
        while True:
            response = (
                service.files()
                .list(
                    q=query,
                    spaces="drive",
                    fields="nextPageToken, files(id, name)",
                    pageToken=page_token,
                )
                .execute()
            )
            files.extend(response.get("files", []))
            page_token = response.get("nextPageToken", None)
            if page_token is None:
                break

    except HttpError as error:
        print(f"An error occurred: {error}")
        files = None

    return files

def list_dirs(query):
    creds = Credentials.from_authorized_user_file("token.json")
    directories = []

    try:
        # Create Drive API client
        service = build("drive", "v3", credentials=creds)
        page_token = None
        while True:
            response = (
                service.files()
                .list(
                    q=query,
                    spaces="drive",
                    fields="nextPageToken, files(id, name)",
                    pageToken=page_token,
                )
                .execute()
            )
            directories.extend(response.get("files", []))
            page_token = response.get("nextPageToken", None)
            if page_token is None:
                break

    except HttpError as error:
        print(f"An error occurred: {error}")
        directories = None

    return directories

def find_id(id):
  creds = Credentials.from_authorized_user_file("token.json")

  try:
    # Create Drive API client
    service = build("drive", "v3", credentials=creds)
    
    # Get file metadata by ID
    file = service.files().get(fileId=id, fields="name").execute()
    
    return {"error_message": None, "file": file}


  except HttpError as error:
    error_message = handle_http_error(error)
    return {"error_message": error_message}
    
# TO DO NOT FINISHED. Handle error message returned from manual_http_error in the exception
def handle_http_error(error):
    """Extract and format error code and message from HttpError."""
    # Extract HTTP status code
    error_code = error.resp.status
    try:
        # Extract the raw response content
        error_content = error.content.decode('utf-8')

        # Parse the JSON content
        error_json = json.loads(error_content)

        # Extract the error message
        error_message = error_json.get('error', {}).get('message', 'No error message found')
    except (json.JSONDecodeError, AttributeError):
         error_message = manual_http_error(error_code) # how to process it better so that when this is returned it will work

    return error_message

def manual_http_error(status):
    # Dictionary to map HTTP status codes to error messages
    error_messages = {
        400: "Bad Request",
        401: "Invalid credentials",
        403: "Access not allowed",
        404: "Directory or file not found",
        500: "Backend error",
        502: "Bad gateway",
        503: "Service Unavailable",
        504: "Gateway Timeout"
    }

    # Return the corresponding error message or a default message
    return error_messages.get(status, f"An HTTP error occurred: {status}")

# files to ignore to not accidentally modify them. 
# TO DO better handling of files that end in .py and .json and .md and . if it is in the app's directory
def ignored_files(file):

    if not os.path.isfile(file):
        return False 
    if file.endswith('.py') or file.endswith('.json'):
        return False
    if file.startswith('.'):
        return False
    if file.endswith('.md'):
        return False
    
    return True

# for resumeable uploads
def resumable(file_path, file_metadata, parent_id):

    creds = Credentials.from_authorized_user_file("../token.json")

    service = build('drive', 'v3', credentials=creds)
    media = MediaFileUpload(file_path, chunksize=1024*1024, resumable=True)
    file_metadata = {'name': os.path.basename(file_path)}

    if parent_id:
        file_metadata['parents'] = [parent_id]

    request = service.files().create(body=file_metadata, media_body=media, fields='id')
    response = None
    while response is None:
            status, response = request.next_chunk()
            if status:
                print(f'Uploaded {int(status.progress() * 100)}%')

  
def create_folder(file_metadata, parent_id=None):
 
  
  creds = Credentials.from_authorized_user_file("../token.json")
  folder_name = file_metadata['name']

  try:
    # create drive api client
    service = build("drive", "v3", credentials=creds)
    file_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
    }
    if parent_id:
        file_metadata['parents'] = [parent_id]

    # pylint: disable=maybe-no-member
    file = service.files().create(body=file_metadata, fields="id").execute()
    print(f'Folder ID: "{file.get("id")}".')
    return file.get("id")

  except HttpError as error:
    print(f"An error occurred: {error}")
    return None
  

  

    



  #add push and pull functions to use in other functions that specify whart users wnats to pull and push

  #make a valid id or valid name function which checks if the id/name user gave actuall exist. can be used for listing or modifying thingd
