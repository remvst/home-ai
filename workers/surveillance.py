import logging

from kik.messages import PictureMessage

import config
from bot.kik_bot import bot
from helpers.video_surveillance import VideoSurveillance
from scripts.welcome_home import generate_string
from utils.ngrok import get_ngrok_url
from web.app import app, path_to_static_file
from workers.speech import add_to_queue


def face_detected(picture_path, enhanced_path):
    logging.info('Face detected')

    url = '{}/{}'.format(get_ngrok_url(), path_to_static_file(enhanced_path))
    bot.send([PictureMessage(pic_url=url, to=config.KIK_BOT_RECIPIENT_USERNAME)])

    string = generate_string()
    add_to_queue(string)

surveillance = VideoSurveillance(pictures_folder='{}/surveillance'.format(app.static_folder))
surveillance.detection_handler = face_detected

def worker():
    while True:
        surveillance.check()
