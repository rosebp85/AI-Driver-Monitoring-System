import math
import time


class EyeTracker:

    LEFT_EYE = [33, 160, 158, 133, 153, 144]
    RIGHT_EYE = [362, 385, 387, 263, 373, 380]

    def __init__(self):

        self.EAR_THRESHOLD = 0.15

        self.closed_frames = 0
        self.blink_count = 0
        self.MIN_CLOSED_FRAMES = 2

        self.eye_closed_start_time = None
        self.closed_duration = 0
        self.DROWSY_THRESHOLD_SECONDS = 2.5

    def distance(self, p1, p2):

        return math.hypot(
            p1.x - p2.x,
            p1.y - p2.y
        )

    def calculate_ear(self, landmarks, eye):

        p1 = landmarks[eye[0]]
        p2 = landmarks[eye[1]]
        p3 = landmarks[eye[2]]
        p4 = landmarks[eye[3]]
        p5 = landmarks[eye[4]]
        p6 = landmarks[eye[5]]

        vertical1 = self.distance(p2, p6)
        vertical2 = self.distance(p3, p5)

        horizontal = self.distance(p1, p4)

        if horizontal == 0:
            return 0

        ear = (vertical1 + vertical2) / (2.0 * horizontal)

        return ear

    def get_ear(self, face_landmarks):

        landmarks = face_landmarks.landmark

        left_ear = self.calculate_ear(
            landmarks,
            self.LEFT_EYE
        )

        right_ear = self.calculate_ear(
            landmarks,
            self.RIGHT_EYE
        )

        return (left_ear + right_ear) / 2

    def is_closed(self, ear):

        return ear < self.EAR_THRESHOLD
    

    def update_blink(
        self,
        closed
    ):

        if closed:
            self.closed_frames += 1

        else:
            if self.closed_frames >= self.MIN_CLOSED_FRAMES:
                self.blink_count += 1

            self.closed_frames = 0

        return self.blink_count
    
    def detect_drowsiness(
        self,
        closed
    ):

        if closed:

            if self.eye_closed_start_time is None:
                self.eye_closed_start_time = time.time()

            self.closed_duration = time.time() - self.eye_closed_start_time

        else:

            self.eye_closed_start_time = None
            self.closed_duration = 0

        is_drowsy = self.closed_duration >= self.DROWSY_THRESHOLD_SECONDS

        return (
            is_drowsy,
            self.closed_duration
        )