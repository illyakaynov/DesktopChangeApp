import logging
import requests
import json
import ctypes
import datetime
import random as rng


def get_image_url(image_date):
    params = {'hd': 'true',
              'date': image_date}

    response = requests.get(api_url_base, params=params)


    if response.status_code == 200:
        data = json.loads(response.content.decode('utf-8'))
        if data['media_type'] == 'image':
            return data['hdurl']
        else:
            log_message = '{}: {} (url: {})'.format(str(datetime.datetime.now())[:16], data['media_type'], data['url'])
            logging.error(log_message)
        return None
    else:
        return None


api_token = 'tPuB5DWqYzZ2a01pNxQbHb8Q2bZD6I81jphtKAuC'
api_url_base = 'https://api.nasa.gov/planetary/apod?api_key={0}'.format(api_token)

logging.basicConfig(filename='errors.log', level=logging.ERROR)

search_date = str(datetime.datetime.now())[:10]

while True:
    image_url = get_image_url(search_date)

    if image_url is not None:
        image_bin = requests.get(image_url)
        with open("python1.png", "wb") as code:
             code.write(image_bin.content)
        image_name = "C:\\Users\\ikayn\\Repositories\\python_progs\\python_test\\python1.png"

        ctypes.windll.user32.SystemParametersInfoW(20, 0, image_name, 0)
        break

    search_date = '{}-{}-{}'.format(rng.randint(2000, 2018), rng.randint(1, 13), rng.randint(1, 28))

