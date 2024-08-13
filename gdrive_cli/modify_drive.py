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
        click.echo(click.style("Error: ", bold=True) + f"File with ID '{file_id}' deleted.")
    except HttpError as error:
        click.echo(click.style("Error: ", bold=True) + f"An error occurred: {error}")
    except Exception as e:
        click.echo(click.style("Error: ", bold=True) + f"{e}")