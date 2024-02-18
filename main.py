import requests
import json
import logging


TOKEN = ('ТокенПокен')


class VKAPIClient:
    API_BASE_URL = 'https://api.vk.com/method'

    def __init__(self, token, user_id):
        self.token = token
        self.user_id = user_id

    def get_common_params_vk(self):
        return {
            'access_token': self.token,
            'v': '5.131'
        }

    def _build_url(self, api_method):
        return f'{self.API_BASE_URL}/{api_method}'

    def get_profile_photos(self):
        params = self.get_common_params_vk()
        params.update({'owner_id': self.user_id, 'album_id': 'profile', 'extended': 1, 'photo_sizes': 1})
        response = requests.get(self._build_url('photos.get'), params=params)
        photos_data = response.json()

        with open('photos_data.json', 'w', encoding='utf-8') as file:
            json.dump(photos_data, file, ensure_ascii=False, indent=4)


class CreateFolder:
    def __init__(self, url_create_dir, authorization_token, name_folder, url_load_yandex_disc):
        self.url_create_dir = url_create_dir
        self.authorization_token = authorization_token
        self.name_folder = name_folder
        self.url_load_yandex_disc = url_load_yandex_disc

    def get_common_params_ya(self):
        return {
            'path': f'{self.name_folder}'
        }

    def get_common_headers_ya(self):
        return {
            'Authorization': f'OAuth {self.authorization_token}'
        }

    def responses_all(self):
        all_responses = requests.put(self.url_create_dir, params=self.get_common_params_ya(),
                                     headers=self.get_common_headers_ya())
        return all_responses

    def upload_photos_from_json(self, json_file):
        logging.basicConfig(filename='photo_upload.log', level=logging.DEBUG, format='%(asctime)s - %(message)s')

        with open(json_file, 'r', encoding='utf-8') as file:
            photos_data = json.load(file)

            for index, photo_info in enumerate(photos_data['response']['items']):
                likes = photo_info.get('likes', {}).get('count', 0)
                photo_url = max(photo_info['sizes'], key=lambda x: x['width'] * x['height'])['url']
                photo_data = requests.get(photo_url).content
                photo_name = f'likes - {likes} - index {index}.jpg'

                upload_params = {
                    'path': f'{self.name_folder}/{photo_name}'
                }

                with open(photo_name, 'wb') as photo_file:
                    photo_file.write(photo_data)

                with open(photo_name, 'rb') as photo_file:
                    response = requests.get(self.url_load_yandex_disc, params=upload_params,
                                            headers=self.get_common_headers_ya())
                    upload_data = response.json()

                    if 'error' in upload_data:
                        print(f"{upload_data['message']}")
                    else:
                        upload_url = upload_data['href']
                        response = requests.put(upload_url, files={'file': photo_file})
                        print(f"Загрузка {photo_name} status code == {response.status_code}")


if __name__ == '__main__':
    id_vk_user = 'АйдиПрийди'
    vk_client = VKAPIClient(TOKEN, id_vk_user)
    vk_client.get_profile_photos()

    token_yandex_disc = 'ТокенПокен'
    url_base = 'https://cloud-api.yandex.net'
    url_create_folder = 'https://cloud-api.yandex.net/v1/disk/resources'
    url_load_ya_disc = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    name_folder_ya_disc = 'Profile_photos_VK'
    ya_disc = CreateFolder(url_create_folder, token_yandex_disc, name_folder_ya_disc, url_load_ya_disc)

    ya_disc.responses_all()
    json_file_path = 'photos_data.json'
    ya_disc.upload_photos_from_json(json_file_path)
