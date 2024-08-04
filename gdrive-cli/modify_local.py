import click
import os
from utils import ignored_files

@click.command('rename', short_help='List directories in Google Drive')
@click.argument('old_name')
@click.argument('new_name')
def rename(old_name, new_name):
    os.rename(old_name, new_name)

# changes extension of all files in directory
@click.command('change', short_help='List directories in Google Drive')
@click.argument('filter', required=False, default=None)
def change_all(filter):
   cur_dir = os.getcwd()
   contents = os.listdir(cur_dir)
   
   for file in contents:
       if ignored_files(file):
           if os.path.splitext(file)[-1] == '':
                new_file = file + filter
                os.rename(file, new_file)
                continue

           name, old_ext = file.rsplit('.', 1)
           new_file = name + filter
           os.rename(file, new_file)
           