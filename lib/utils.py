import cv2
import httplib2
import json
import logging
import os
import psutil
import StringIO
import subprocess
import sys

import pygame
import pygame.camera
from skimage.measure import compare_ssim

def is_user_in_network(mac_address, timeout=5000):
    arp_scan = subprocess.check_output([
        'arp-scan',
        '-l',
        '--timeout={}'.format(timeout)
    ])
    return mac_address in arp_scan

def get_ngrok_url():
    tunnels_url='http://localhost:4040/api/tunnels'

    http = httplib2.Http()
    resp, content = http.request(tunnels_url)

    assert resp.status == 200

    json_response = json.loads(content)

    return json_response['tunnels'][0]['public_url']

def run_ngrok(port):
    subprocess.check_output(['./ngrok', 'http', str(port)])

def restart_process():
    logging.info('Restarting process')

    try:
        p = psutil.Process(os.getpid())
        for handler in p.get_open_files() + p.connections():
            os.close(handler.fd)
    except Exception as e:
        logging.error(e)

    python = sys.executable
    os.execl(python, python, *sys.argv)

CAMERA_INITIALIZED = False

def take_picture(destination, skip=1):
    global CAMERA_INITIALIZED

    if not CAMERA_INITIALIZED:
        pygame.camera.init()
        CAMERA_INITIALIZED = True

    cameras = pygame.camera.list_cameras()
    if len(cameras) == 0:
        raise Exception('No cameras detected, unable to take picture')

    camera = pygame.camera.Camera(cameras[0])
    camera.start()

    # Skip frames
    for i in xrange(skip):
        camera.get_image()

    # Actually capture
    img = camera.get_image()
    pygame.camera.quit()

    # Save to disk
    pygame.image.save(img, destination)

def compare_images(a, b):
    return compare_ssim(a, b)
