import requests
import json


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

    def authenticate_by_id_or_screen_name(self):
        url = f"https://api.vk.com/method/users.get?user_ids={self.user_id}&access_token={self.token}&v=5.131"
        response = requests.get(url)

        if response.status_code == 200:
            user_data = response.json()
            id_user = user_data['response'][0]['id']
            print(id_user)
            return self.get_profile_photos(id_user)
        else:
            return None

    def get_profile_photos(self, id_user):
        photos_params = self.get_common_params_vk()
        photos_params.update({'owner_id': id_user, 'album_id': 'profile', 'extended': 1, 'photo_sizes': 1})
        photos_response = requests.get(self._build_url('photos.get'), params=photos_params)
        photos_data = photos_response.json()

        with open('photos_data.json', 'w', encoding='utf-8') as file:
            json.dump(photos_data, file, ensure_ascii=False, indent=4)