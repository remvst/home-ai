import os
from datetime import datetime

from utils.camera import take_picture
from utils.content import PictureURLContent
from utils.ngrok import get_ngrok_url
from utils.script import Script


class TakePictureScript(Script):

    def __init__(self, static_folder, *args, **kwargs):
        super(TakePictureScript, self).__init__(*args, **kwargs)
        self.static_folder = static_folder

    def run(self, input_content):
        now = datetime.utcnow()
        pic_id = now.isoformat()

        relative_path = '{}/pictures/{}.jpg'.format(self.static_folder, pic_id)
        take_picture(relative_path)

        url = '{}/{}'.format(get_ngrok_url(), self._path_to_static_file(relative_path))

        self.output([PictureURLContent(picture_url=url)])

    def _path_to_static_file(self, relative_path):
        path_from_static = os.path.relpath(relative_path, self.static_folder)
        return 'static/{}'.format(path_from_static)
