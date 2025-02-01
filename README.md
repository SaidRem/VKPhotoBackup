# VK Photo Backup to Yandex Disk

## Description

This script allows you to back up photos from a VK.com user account to Yandex Disk or save them locall on your PC.

## Features

- Fetches photos from a VK user profile
- Saves photos locally with names based on the number of likes
- Handles duplicate file names by appending the upload date from the metadata
- Uploads photos to Yandex Disk in a folder named with the current date and time
- Saves metadata about the uploaded photos in a JSON file

## Prerequisites

You need to have the following installed:

- Python 3.x
- Required Python libraries (see `requirements.txt`)
- VK API access token
- Yandex Disk API token

## Installation

1. Clone this repository:

   ```sh
   git clone https://github.com/SaidRem/VKPhotoBackup.git
   cd VKPhotoBackup
   ```

2. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

3. Create a file `VK_TOKEN.json` in the project directory and insert your VK token:

   ```json
   {
       "VK_ACCESS_TOKEN": "your_secret_token_here"
   }
   ```

## Usage

Run the script:

```sh
python main.py
```

This will:

- Prompt you to enter the VK user ID from whose profile you want to take photos
- Prompt you to enter the Yandex Disk token
- Download photos from VK
- Upload them to Yandex Disk
- Save metadata to `photos_metadata.json`

## Configuration

By default, the script fetches up to **5 photos** from the VK profile. You can change this limit in the script or pass it as an argument.

## Requirements

The `requirements.txt` file includes:

```
requests
```

## License

This project is licensed under the MIT License.

