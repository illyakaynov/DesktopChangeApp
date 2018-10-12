import logging
import requests
import json
import ctypes
import datetime
import random as rng
import os
from shutil import copyfile

api_token = 'tPuB5DWqYzZ2a01pNxQbHb8Q2bZD6I81jphtKAuC'
api_url_base = 'https://api.nasa.gov/planetary/apod'

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
saved_wallpapers_path = os.path.join(ROOT_DIR, 'saved_wallpapers')
temp_image_path = os.path.join(ROOT_DIR, 'temp\\current_image.png')
json_path = os.path.join(ROOT_DIR, 'temp\\data.json')

logging.basicConfig(filename='logs\\errors.log', level=logging.ERROR)


def set_random_wallpaper():
    date = get_random_date()

    while True:
        data = get_json_from_api(api_url_base, api_token, date)
        if data['media_type'] == 'image':
            fetch_image(data['hdurl'], temp_image_path)
            change_wallpaper_to_image(temp_image_path)
            save_image_data(data, json_path)
            break
        date = get_random_date()


def save_current_image():
    copyfile(temp_image_path, os.path.join(saved_wallpapers_path, get_image_name(json_path) + '.png'))


def get_json_from_api(api_url, token, date):
    params = {'api_key': token,
              'hd': 'true',
              'date': date}

    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        current_json_response = json.loads(response.content.decode('utf-8'))
        return current_json_response
    log_message = 'Wrong request, status code: ({}) date: {}'.format(response.status_code, date)
    logging.error(log_message)


def fetch_image(url, temp_path):
    image_bin = requests.get(url)

    with open(temp_path, "wb") as f:
        f.write(image_bin.content)


def save_image_data(json_data, path):
    with open(path, 'w') as outfile:
        json.dump(json_data, outfile)


def get_random_date():
    return '{}-{}-{}'.format(rng.randint(2000, 2018), rng.randint(1, 13), rng.randint(1, 28))


def change_wallpaper_to_image(path):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
    print('wallpaper was successfully changed')


def create_saved_wallpapers_folder_if_not_exists():
    if not os.path.exists("saved_wallpapers"):
        os.makedirs("saved_wallpapers")


def create_temp_folder_if_not_exist():
    if not os.path.exists("temp"):
        os.makedirs("temp")



def get_image_name(data_path):
    with open(data_path) as f:
        json_data = json.load(f)
    print(json_data['title'].replace(' ', '_'))
    return json_data['title'].replace(' ', '_').replace(':', '_')


create_saved_wallpapers_folder_if_not_exists()

create_temp_folder_if_not_exist()


