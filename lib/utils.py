import httplib2
import json
import subprocess

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

    return json_response['tunnels'][0]['public_url']:

def run_ngrok(port):
    subprocess.check_output(['./ngrok', 'http', str(port)])
