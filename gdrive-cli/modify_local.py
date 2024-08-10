import click
import os
from utils import ignored_files

#renames files and directories 
@click.command('rename', short_help='renames')
@click.argument('old_name')
@click.argument('new_name')
@click.option('--d', is_flag=True, help='Indicate if the target is a directory')
def rename(old_name, new_name, d):
    if d:
        os.renames(old_name, new_name)
    os.rename(old_name, new_name)

# changes extension of all files in directory
@click.command('change', short_help='changes all files to specified extension')
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

