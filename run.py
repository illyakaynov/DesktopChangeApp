import wallpaper_changer as wc
import sys
import click

commands = {'current': wc.set_current_APOD,
            'random': wc.set_random_wallpaper,
            'save': wc.save_current_image,
            'info': wc.get_image_info}


@click.command()
@click.argument('command')
def run(command):
    commands.get(command, no_such_command)()


def no_such_command():
    print('No such command. Use current, random or save')

if __name__ == "__main__":
    run()