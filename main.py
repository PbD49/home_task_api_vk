from vk_save_json import VKAPIClient
from folder import CreateFolder, UploadPhotos
import configparser


config = configparser.ConfigParser()
config.read('tokens.ini')


token_vk = config['Tokens']['token_vk']
token_yandex_disc = config['Tokens']['token_yandex_disc']


if __name__ == '__main__':
    id_vk_user = (input('Введите ID для загрузки: '))
    vk_client = VKAPIClient(token_vk, id_vk_user)
    vk_client.authenticate_by_id_or_screen_name()

    url_create_folder = 'https://cloud-api.yandex.net/v1/disk/resources'
    url_load_ya_disc = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    name_folder_ya_disc = 'Profile_photos_VK'
    ya_disc_create_folder = CreateFolder(url_create_folder, token_yandex_disc, name_folder_ya_disc, url_load_ya_disc)
    ya_disc_create_folder.responses_all()

    ya_disc_upload_photos = UploadPhotos(url_create_folder, token_yandex_disc, name_folder_ya_disc, url_load_ya_disc)
    count_photo: int = int(input('Введите количество фотографий для загрузки: '))
    json_file_path = 'photos_data.json'
    ya_disc_upload_photos.upload_photos_from_json(json_file_path, count_photo)