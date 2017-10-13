import cv2
import os
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
        print 'survey start'

        now = datetime.utcnow()
        pic_id = now.isoformat()

        picture_path = '{}/{}-picture.jpg'.format(self.pictures_folder, pic_id)
        enhanced_path = '{}/{}-enhanced.jpg'.format(self.pictures_folder, pic_id)

        take_picture(picture_path)

        picture = cv2.imread(picture_path)
        enhanced = picture.copy()
        grayscale = cv2.cvtColor(picture, cv2.COLOR_BGR2GRAY)

        faceCascade = cv2.CascadeClassifier('assets/haarcascade_frontalface_default.xml')

        faces = faceCascade.detectMultiScale(
            grayscale,
            scaleFactor=1.1,
            minNeighbors=5
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(enhanced, (x, y), (x + w, y + h), (0, 0, 255), 2)

        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        humans, weights = hog.detectMultiScale(grayscale, winStride=(4, 4), padding=(8, 8), scale=1.05)

        for (x, y, w, h) in humans:
            cv2.rectangle(enhanced, (x, y), (x + w, y + h), (0, 0, 255), 2)

        cv2.imwrite(enhanced_path, enhanced)

        print 'survey end'

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
