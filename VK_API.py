import os
import json
import requests


class VKPhotoFetcher:
    BASE_URL = "https://api.vk.com/method/photos.get"

    def __init__(self, access_token, user_id, save_dir="vk", exporter=None):
        """
        Initializes VKPhotoFetcher with API credentials and save directory.
        """
        self.access_token = access_token
        self.user_id = user_id
        if not exporter:
            self._exporter = exporter
            self.save_dir = save_dir
            os.makedirs(self.save_dir, exist_ok=True)
        else:
            self._exporter = exporter

    def fetch_photos(self, album_id="profile", version="5.131", limit=5):
        """
        Fetches photos from the given VK album.
        """
        params = {
            "owner_id": self.user_id,
            "album_id": album_id,
            "extended": 1,  # To get number of likes
            "photo_sizes": 1,  # To get all size variants
            "access_token": self.access_token,
            "v": version,
        }

        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

            if "response" in data:
                return data["response"]["items"][:limit]
            else:
                raise ValueError(f"VK API Error: {data}")
        except requests.RequestException as e:
            raise ConnectionError(f"Network error: {e}")
        except ValueError as e:
            raise RuntimeError(f"Data processing error: {e}")

    @staticmethod
    def _extract_highest_res_photo(photo):
        """
        Extracts the highest resolution photo and
        returns its URL and size type.
        """
        best_photo = max(photo["sizes"], key=lambda x: x["height"]*x["width"])
        return best_photo["url"], best_photo["type"]

    def download_photos(self):
        """
        Downloads photos and saves metadata in a JSON file.
        """
        photos = self.fetch_photos()
        metadata = []

        for photo in photos:
            photo_url, size_type = self._extract_highest_res_photo(photo)
            likes = photo["likes"]["count"]
            file_name = f"{likes}.jpg"
            file_path = os.path.join(self.save_dir, file_name)

            # Download photo
            try:
                response = requests.get(photo_url, stream=True)
                response.raise_for_status()
                with open(file_path, "wb") as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)

                # Save metadata
                metadata.append({"file_name": file_name, "size": size_type})
                print(f"Downloaded: {file_name}")
            except requests.RequestException as e:
                print(f"Failed to download {photo_url}: {e}")

        # Save metadata to JSON
        json_path = "photos_metadata.json"
        with open(json_path, "w", encoding="utf-8") as json_file:
            json.dump(metadata, json_file, indent=4, ensure_ascii=False)

        print(f"Metadata saved to {json_path}")

    def export(self, limit=5):
        if not self._exporter:
            print("Do not have exporter")
            return

        photos = self.fetch_photos(limit=limit)
        metadata = []
        file_names = []

        for photo in photos:
            photo_url, size_type = self._extract_highest_res_photo(photo)
            likes = photo["likes"]["count"]
            file_name = f"{likes}.jpg"
            if file_name in file_names:
                file_name = f"{likes}_{photo['date']}.jpg"
                file_names.append((photo_url, file_name, size_type))
            else:
                file_names.append((photo_url, file_name, size_type))

        self._exporter.create_folder()

        for url, file_name, size_type in file_names:
            try:
                self._exporter.upload_from_url(url, file_name)
                metadata.append({"file_name": file_name, "size": size_type})
                print(f"Uploaded to disk: {file_name}")
            except requests.RequestException as e:
                print(f"Failed to upload {url}: {e}")

        # Save metadata to JSON
        json_path = "photos_metadata.json"
        with open(json_path, "w", encoding="utf-8") as json_file:
            json.dump(metadata, json_file, indent=4, ensure_ascii=False)

        print(f"Metadata saved to {json_path}")


# Example Usage
if __name__ == "__main__":
    ACCESS_TOKEN = "enter your token"  # Replace with your token from vk
    USER_ID = "enter id"   # Replace with the actual VK user ID

    vk_fetcher = VKPhotoFetcher(ACCESS_TOKEN, USER_ID)
    vk_fetcher.download_photos()
