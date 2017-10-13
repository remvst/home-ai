import httplib2
import json
import logging
import os
import psutil
import subprocess
import sys


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

def take_picture(destination, skip=1, resolution=(1280, 720)):
    subprocess.check_output([
        'fswebcam',
        '-r', '{}x{}'.format(resolution[0], resolution[1]),
        '--skip', '1',
        '--frames', '1',
        '--no-banner',
        '--quiet',
        destination
    ])

def compare_images(a, b):
    from skimage.measure import compare_ssim
    return compare_ssim(a, b)
