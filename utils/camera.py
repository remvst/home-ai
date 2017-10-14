import logging
import subprocess

def take_picture(destination, skip=1, resolution=(1280, 720)):
    logging.debug('Taking picture')
    subprocess.check_output([
        'fswebcam',
        '-r', '{}x{}'.format(resolution[0], resolution[1]),
        '--skip', str(skip),
        '--frames', '5',
        '--no-banner',
        '--quiet',
        destination
    ])
