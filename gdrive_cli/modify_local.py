import click
import os
from gdrive_cli.utils import ignored_files

#renames files and directories 
@click.command('rename', short_help='renames')
@click.argument('old_name')
@click.argument('new_name')
@click.option('--d', is_flag=True, help='Indicate if the target is a directory')
def rename(old_name, new_name, d):
    
    if not os.path.exists(old_name):
        click.echo(click.style("Error: ", bold=True) + f" The file or directory '{old_name}' does not exist.")
        return

    if os.path.exists(new_name):
        click.echo(click.style("Error: ", bold=True) + f" The file or directory '{new_name}' already exists.")
        return

    try:
        if d:
            os.renames(old_name, new_name)
        os.rename(old_name, new_name)
    except PermissionError:
        click.echo(click.style("Error:", bold=True) + " Permission denied to change name. Check file/directory permissions.")
    except Exception as e:
        click.echo(click.style("Error:", bold=True) + f" Unexpected error: {e}")

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
           try:
               os.rename(file, new_file)
           except PermissionError:
               click.echo(click.style("Error:", bold=True) + " Permission denied to change name. Check file/directory permissions.")
           except Exception as e:
               click.echo(click.style("Error:", bold=True) + f" Unexpected error: {e}")

