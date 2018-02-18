import httplib2
import json
import subprocess


def get_ngrok_url():
    tunnels_url ='http://localhost:4040/api/tunnels'

    http = httplib2.Http()
    resp, content = http.request(tunnels_url)

    assert resp.status == 200

    json_response = json.loads(content)

    return json_response['tunnels'][0]['public_url']


def run_ngrok(port):
    subprocess.check_output(['./ngrok', 'http', str(port)])
