import math


class YawnDetector:

    def __init__(self):

        self.MAR_THRESHOLD = 0.55
        self.yawn_count = 0
        self.yawn_frames = 0
        self.MIN_YAWN_FRAMES = 15
        self.yawn_active = False

        self.MOUTH = {
            "left": 61,
            "right": 291,
            "top": 13,
            "bottom": 14,
            "top_inner": 82,
            "bottom_inner": 87
        }

    def distance(
        self,
        p1,
        p2
    ):

        return math.hypot(
            p1.x - p2.x,
            p1.y - p2.y
        )

    def calculate_mar(
        self,
        face_landmarks
    ):

        landmarks = face_landmarks.landmark

        left = landmarks[self.MOUTH["left"]]
        right = landmarks[self.MOUTH["right"]]

        top = landmarks[self.MOUTH["top"]]
        bottom = landmarks[self.MOUTH["bottom"]]

        top_inner = landmarks[self.MOUTH["top_inner"]]
        bottom_inner = landmarks[self.MOUTH["bottom_inner"]]

        horizontal = self.distance(
            left,
            right
        )

        vertical_1 = self.distance(
            top,
            bottom
        )

        vertical_2 = self.distance(
            top_inner,
            bottom_inner
        )

        if horizontal == 0:
            return 0

        mar = (
            vertical_1 +
            vertical_2
        ) / (
            2 * horizontal
        )

        return mar

    def detect(
        self,
        face_landmarks
    ):

        mar = self.calculate_mar(
            face_landmarks
        )

        is_mouth_open = mar > self.MAR_THRESHOLD

        if is_mouth_open:
            self.yawn_frames += 1

        else:
            if self.yawn_frames >= self.MIN_YAWN_FRAMES:
                self.yawn_count += 1

            self.yawn_frames = 0

        is_yawning = self.yawn_frames >= self.MIN_YAWN_FRAMES

        return (
            mar,
            is_mouth_open,
            is_yawning,
            self.yawn_count
        )