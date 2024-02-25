from datetime import datetime
from io import BytesIO

import requests
import json
import logging


class CreateFolder:
    def __init__(self, url_create_dir, token, name_folder, url_load_yandex_disc):
        self.url_create_dir = url_create_dir
        self.token = token
        self.name_folder = name_folder
        self.url_load_yandex_disc = url_load_yandex_disc

    def get_common_params_ya(self):
        return {
            'path': f'{self.name_folder}'
        }

    def get_common_headers_ya(self):
        return {
            'Authorization': f'OAuth {self.token}'
        }

    def responses_all(self):
        all_responses = requests.put(self.url_create_dir, params=self.get_common_params_ya(),
                                     headers=self.get_common_headers_ya())
        return all_responses


class UploadPhotos(CreateFolder):
    def upload_photos_from_json(self, json_file, count):
        logging.basicConfig(filename='photo_upload.log', level=logging.DEBUG, format='%(asctime)s - %(message)s')

        with open(json_file, 'r', encoding='utf-8') as file:
            photos_data = json.load(file)

            uploaded_count = 0
            unique_counter = 0
            for photo_info in photos_data['response']['items']:
                likes = photo_info.get('likes', {}).get('count', 0)
                photo_url = max(photo_info['sizes'], key=lambda x: x['width'] * x['height'])['url']
                photo_data = requests.get(photo_url).content

                photo_date = datetime.fromtimestamp(photo_info['date']).strftime('%Y-%m-%d')
                photo_name = f'likes - {likes} - {photo_date} - {unique_counter}.jpg'

                if uploaded_count < int(count):
                    upload_params = {
                        'path': f'{self.name_folder}/{photo_name}'
                    }

                    photo_file = BytesIO(photo_data)

                    response = requests.get(self.url_load_yandex_disc, params=upload_params,
                                            headers=self.get_common_headers_ya())
                    upload_data = response.json()

                    if 'error' in upload_data:
                        print(f"{upload_data['message']}")
                    else:
                        upload_url = upload_data['href']
                        response = requests.put(upload_url,
                                                files={'file': photo_file})
                        print(f"Загрузка {photo_name} status code == {response.status_code}")
                        uploaded_count += 1
                        unique_counter += 1
                else:
                    break