import os
import datetime
import requests


class YandexDiskUploader:
    BASE_URL = "https://cloud-api.yandex.net/v1/disk"

    def __init__(self, token):
        """
        Initialize the uploader with a Yandex OAuth token.
        """
        self.headers = {"Authorization": f"OAuth {token}"}
        self.folder_name = self._generate_folder_name()

    @staticmethod
    def _generate_folder_name():
        """
        Generate a folder name using the current date and time.
        """
        return datetime.datetime.now().strftime("Backup_files_%Y-%m-%d_%H-%M-%S")

    def create_folder(self):
        """
        Create a folder on Yandex Disk.
        """
        url = f"{self.BASE_URL}/resources"
        params = {"path": self.folder_name}
        response = requests.put(url, headers=self.headers, params=params)

        if response.status_code == 201:
            print(f"Folder '{self.folder_name}' created successfully.")
        elif response.status_code == 409:
            print(f"Folder '{self.folder_name}' already exists.")
        else:
            print(f"Error creating folder: {response.json()}")

    def upload_file(self, local_file_path):
        """
        Upload a local file to Yandex Disk.
        """
        file_name = os.path.basename(local_file_path)
        upload_path = f"{self.folder_name}/{file_name}"

        url = f"{self.BASE_URL}/resources/upload"
        params = {"path": upload_path, "overwrite": "true"}
        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code == 200:
            upload_url = response.json().get("href")

            with open(local_file_path, "rb") as file:
                upload_response = requests.put(upload_url, files={"file": file})

            if upload_response.status_code == 201:
                print(f"File '{file_name}' uploaded successfully.")
            else:
                print(f"Error uploading file: {upload_response.json()}")
        else:
            print(f"Error getting upload URL: {response.json()}")

    def upload_from_url(self, url_file, file_name):
        """
        Upload a photo to Yandex Disk directly from a URL.
        """
        upload_path = f"{self.folder_name}/{file_name}"

        url = f"{self.BASE_URL}/resources/upload"
        params = {
            "path": upload_path,
            "url": url_file,
            "overwrite": "true"
        }

        response = requests.post(url, headers=self.headers, params=params)

        if response.status_code == 202:
            print(f"File '{file_name}' uploaded successfully from URL.")
        else:
            print(f"Error uploading from URL: {response.json()}")


# Example Usage
if __name__ == "__main__":
    TOKEN = ""  # Replace with your Yandex Disk token

    uploader = YandexDiskUploader(TOKEN)
    uploader.create_folder()

    # Example: Upload a local file
    uploader.upload_file("enter your path to a file")

    # Example: Upload from URL
    uploader.upload_from_url("enter url to file", "photo_from_url.jpg")
