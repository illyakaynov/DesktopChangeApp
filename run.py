import wallpaper_changer as wc
import sys

while(True):
    command = input('Enter your command:\n')
    if command == 'random':
        wc.set_random_wallpaper()
    elif command == 'save':
        wc.save_current_image()
    elif command == 'exit':
        break
    elif command == 'current':
        wc.set_current_APOD()




