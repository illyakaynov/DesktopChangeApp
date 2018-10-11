from wallpaper_changer import WallpaperChanger
import sys

wc = WallpaperChanger()



while(True):
    command = input('Enter your command:\n')
    if command == 'random':
        wc.set_random_wallpaper()
    elif command == 'save':
        wc.save_image()
    elif command == 'exit':
        break




