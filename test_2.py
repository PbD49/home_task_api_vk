import requests


class VK:
    def __init__(self, token, user_id, version='5.131'):
        self.token = token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def users_info(self):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params, **params})
        return response.json()


access_token = ('ТокенПокен')

id_user = 'АйдиПрийди'
vk = VK(access_token, id_user)

print(vk.users_info())


