import cv2
import os
import threading
from datetime import datetime, timedelta

from utils.camera import take_picture

DEFAULT_MIN_DETECTION_INTERVAL = timedelta(seconds=30)

class VideoSurveillance(object):

    def __init__(self, pictures_folder, min_detection_interval=DEFAULT_MIN_DETECTION_INTERVAL):
        super(VideoSurveillance, self).__init__()
        self.pictures_folder = pictures_folder
        self.min_detection_interval = min_detection_interval
        self.detection_handler = None
        self.last_detection = datetime.utcnow() - self.min_detection_interval

    def survey(self):
        now = datetime.utcnow()
        pic_id = now.isoformat()

        picture_path = '{}/{}-picture.jpg'.format(self.pictures_folder, pic_id)
        enhanced_path = '{}/{}-enhanced.jpg'.format(self.pictures_folder, pic_id)

        take_picture(picture_path, resolution=(640, 360))

        picture = cv2.imread(picture_path)
        enhanced = picture.copy()
        grayscale = cv2.cvtColor(picture, cv2.COLOR_BGR2GRAY)

        faces = []
        profiles = []

        def faces_worker():
            face_cascade = cv2.CascadeClassifier('assets/haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(
                grayscale,
                scaleFactor=1.1,
                minNeighbors=5
            )

        def profiles_worker():
            profile_cascade = cv2.CascadeClassifier('assets/haarcascade_profileface.xml')
            profiles = profile_cascade.detectMultiScale(
                grayscale,
                scaleFactor=1.1,
                minNeighbors=5
            )

        faces_thread = threading.Thread(target=faces_worker)
        profiles_thread = threading.Thread(target=profiles_worker)

        faces_thread.start()
        profiles_thread.start()

        faces_thread.join()
        profiles_thread.join()

        for (x, y, w, h) in faces:
            cv2.rectangle(enhanced, (x, y), (x + w, y + h), (0, 0, 255), 2)

        for (x, y, w, h) in profiles:
            cv2.rectangle(enhanced, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imwrite(enhanced_path, enhanced)

        return picture_path, enhanced_path, len(faces) > 0

    def check(self):
        picture_path, enhanced_path, detected = self.survey()

        # Delete unnecessary pictures
        if not detected:
            os.remove(picture_path)
            os.remove(enhanced_path)
            return

        now = datetime.utcnow()
        time_since_last_detection = now - self.last_detection
        should_fire = time_since_last_detection > self.min_detection_interval
        self.last_detection = now

        if self.detection_handler is not None and should_fire:
            self.detection_handler(picture_path=picture_path, enhanced_path=enhanced_path)
