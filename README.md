# Google Drive CLI Tool

## Description

This is a simple command-line app for the Google Drive API. It also allows people to modify the filenames/extensions of files on their computer, ideally before uploading.

## Features

This project uses a custom Click command named `gdrive` for it to run. `gdrive` arguments:

- **login** - Authenticates you to your account.
- **logout** - Logs out by removing `token.json` files, which means you will have to login on next use.
- **list** - Lists files/directories in your Google Drive.
- **search** - Searches for specific files by ID, name, or extension type.
- **rename** - Lets you rename a specified file stored locally.
- **change** - Lets you change the extension of a specified file stored locally.
- **download** - Lets you download files and folders from Google Drive.
- **upload** - Lets you upload files or directories and their files

## Current Status

Not yet complete. This is just the beginning of this project.
