# VK Photo Backup to Yandex Disk

## Description

This Python project automates the backup of photos from a VK.com user account to Yandex Disk. It retrieves photos from the VK profile, saves them locally, and uploads them to Yandex Disk. The photos are named based on the number of likes, and if multiple photos have the same number of likes, the upload date is added to the filename. A JSON file is also created to store metadata about the uploaded photos.

## Features

- Fetches photos from a VK.com profile.
- Saves photos locally with meaningful filenames (`likes_date.jpg` if necessary).
- Uploads photos to Yandex Disk in a folder named with the current date and time.
- Generates a `photos.json` file with metadata about the saved photos.
- Supports secure token storage.
- Allows limiting the number of fetched photos (default: 5).

## Requirements

- Python 3.x
- `requests` library (`pip install requests`)
