import logging

from helpers.video_surveillance import VideoSurveillance
from utils.ngrok import get_ngrok_url
from workers.web_server import path_to_static_file


def face_detected(picture_path, enhanced_path):
    logging.info('Face detected')
    url = '{}/{}'.format(get_ngrok_url(), path_to_static_file(enhanced_path))
    bot_output.output_picture(url)

    ScriptRunner(came_home_script, output=speech_output).run()

surveillance = VideoSurveillance(pictures_folder='{}/surveillance'.format(static_folder))
surveillance.detection_handler = face_detected

def worker():
    while True:
        surveillance.check()
