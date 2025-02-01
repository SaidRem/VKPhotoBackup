import json

from YaDiskAPI import YandexDiskUploader
from VK_API import VKPhotoFetcher


def main():
    with open("VK_TOKEN.json", "r") as file:
        config = json.load(file)

    ACCESS_TOKEN = config.get("VK_ACCESS_TOKEN")

    user_id = input("Enter vk user id: ")
    token_ya_disk = input("Enter yandex disk token: ")

    vk_backup = VKPhotoFetcher(access_token=ACCESS_TOKEN,
                               user_id=user_id,
                               exporter=YandexDiskUploader(token_ya_disk))
    vk_backup.export(limit=5)


if __name__ == "__main__":
    main()
