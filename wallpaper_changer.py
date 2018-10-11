import logging
import requests
import json
import ctypes
import datetime
import random as rng
import os
from shutil import copyfile


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class WallpaperChanger:


    def __init__(self):
        self.api_token = 'tPuB5DWqYzZ2a01pNxQbHb8Q2bZD6I81jphtKAuC'
        self.api_url_base = 'https://api.nasa.gov/planetary/apod?api_key={0}'.format(self.api_token)
        # logging.basicConfig(filename='logs\\errors.log', level=logging.ERROR)

        self.load_last_image_data()

        self.date = str(datetime.datetime.now())[:10]
        self.current_image_url = None
        self.current_image_path = os.path.join(ROOT_DIR, 'saved_wallpapers\\current_image.png')

    def set_random_date(self):
        self.date = '{}-{}-{}'.format(rng.randint(2000, 2018), rng.randint(1, 13), rng.randint(1, 28))

    def fetch_image(self):

        image_bin = requests.get(self.current_image_url)
        with open(self.current_image_path, "wb") as f:
            f.write(image_bin.content)


    def change_wallpaper_to_image(self):
        with open(os.path.join(ROOT_DIR, 'data.json'), 'w') as outfile:
            json.dump(self.current_json_response, outfile)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, self.current_image_path, 0)
        print('wallpaper was successfully changed')


    def random_date(self, from_date, to_date):
        pass

    def set_image_url(self, data):
            if data['media_type'] == 'image':
                self.image_title = data['title']
                self.current_image_url = data['hdurl']
                return self.current_image_url
            log_message = '{}: {} (url: {})'.format(str(datetime.datetime.now())[:16], data['media_type'], data['url'])
            logging.error(log_message)

    def get_json_from_api(self):
        params = {'hd': 'true',
                  'date': self.date}

        response = requests.get(self.api_url_base, params=params)

        if response.status_code == 200:
            self.current_json_response = json.loads(response.content.decode('utf-8'))
            return self.current_json_response
        log_message = 'Wrong request, status code: ({}) date: {}'.format(response.status_code, self.date)
        logging.error(log_message)
        return None

    def set_random_wallpaper(self):
        self.set_random_date()

        while(True):
            self.get_json_from_api()
            if self.current_json_response['media_type'] == 'image':
                self.current_image_url = self.current_json_response['hdurl']
                self.fetch_image()
                self.change_wallpaper_to_image()
                break
            self.set_random_date()

    def createStoredBackgroundsFolderIfNotExists(self):
        if not os.path.exists("saved_wallpapers"):
            os.makedirs("saved_wallpapers")

    def save_image(self):
        self.load_last_image_data()
        copyfile(self.current_image_path, os.path.join(ROOT_DIR, 'saved_wallpapers\\{}.png'.format(self.current_json_response['title'])))
        print('saved image name: saved_wallpapers\\{}.png'.format(self.current_json_response['title']))

    def load_last_image_data(self):
        with open(os.path.join(ROOT_DIR, 'data.json')) as f:
            self.current_json_response = json.load(f)



