import json
import logging
import os

from flask import Flask, request
from kik.messages import messages_from_json

import config

static_folder = '{}/{}'.format(os.path.dirname(os.path.abspath(__file__)), '../static')

app = Flask(__name__, static_folder=static_folder)

def path_to_static_file(relative_path):
    path_from_static = os.path.relpath(relative_path, app.static_folder)
    return 'static/{}'.format(path_from_static)
