import cv2
import os


class FaceDetector:

    def __init__(self):
        cascade_path = os.path.join(
            "assets",
            "haarcascade_frontalface_default.xml"
        )

        self.face_model = cv2.CascadeClassifier(
            cascade_path
        )

    def detect(self, frame):

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        faces = self.face_model.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5
        )

        return faces