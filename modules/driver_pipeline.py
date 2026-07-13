import cv2
import time

from modules.face_mesh import FaceMeshDetector
from modules.head_pose import HeadPoseEstimator
from modules.head_direction import HeadDirectionClassifier
from modules.calibration import HeadCalibration
from modules.eye_tracker import EyeTracker
from modules.yawn_detector import YawnDetector
from modules.driver_behavior import DriverBehavior


class DriverPipeline:

    def __init__(self):

        self.mesh_detector = FaceMeshDetector()
        self.head_pose = HeadPoseEstimator()
        self.direction = HeadDirectionClassifier()
        self.calibration = HeadCalibration()
        self.eye_tracker = EyeTracker()
        self.yawn_detector = YawnDetector()
        self.driver_behavior = DriverBehavior()
        self.calibration_start_time = time.time()
        self.CALIBRATION_SECONDS = 3

    def process(self, frame):

        status = "CALIBRATING"
        alert = None
        head_direction = "CENTER"
        eyes_state = "OPEN"
        yawn_state = "NO"
        eye_closed_time = 0
        head_off_road_time = 0
        yawn_count_window = 0

        results = self.mesh_detector.process(frame)

        if results.multi_face_landmarks:

            face_landmarks = results.multi_face_landmarks[0]

            h, w, _ = frame.shape

            (
                success,
                yaw,
                pitch,
                roll,
                rotation_vector,
                rotation_matrix,
                translation_vector,
                camera_matrix,
                dist_matrix
            ) = self.head_pose.estimate_pose(
                face_landmarks,
                w,
                h
            )

            if success:

                self.calibration.update(
                    yaw,
                    pitch
                )

                if self.calibration.finished:

                    yaw, pitch = self.calibration.normalize(
                        yaw,
                        pitch
                    )

                    if pitch > 180:
                        pitch -= 360

                    if yaw > 180:
                        yaw -= 360

                    head_direction = self.direction.classify(
                        yaw,
                        pitch
                    )

                    ear = self.eye_tracker.get_ear(
                        face_landmarks
                    )

                    eyes_closed = self.eye_tracker.is_closed(
                        ear
                    )

                    self.eye_tracker.update_blink(
                        eyes_closed
                    )

                    self.eye_tracker.detect_drowsiness(
                        eyes_closed
                    )

                    mar, mouth_open, is_yawning, yawn_count = self.yawn_detector.detect(
                        face_landmarks
                    )

                    behavior = self.driver_behavior.update(
                        eyes_closed,
                        head_direction,
                        is_yawning
                    )

                    status = behavior["status"]
                    alert = behavior["alert"]
                    eye_closed_time = behavior["eye_closed_time"]
                    head_off_road_time = behavior["head_off_road_time"]
                    yawn_count_window = behavior["yawn_count"]

                    eyes_state = "CLOSED" if eyes_closed else "OPEN"
                    yawn_state = "YES" if is_yawning else "NO"

                nose_point = (
                    int(face_landmarks.landmark[1].x * w),
                    int(face_landmarks.landmark[1].y * h)
                )

                frame = self.head_pose.draw_axes(
                    frame,
                    nose_point,
                    rotation_vector,
                    translation_vector,
                    camera_matrix,
                    dist_matrix
                )

        frame = self.mesh_detector.draw(
            frame,
            results
        )

        calibration_remaining = max(
            0,
            self.CALIBRATION_SECONDS - int(time.time() - self.calibration_start_time)
        )

        return {
            "frame": frame,
            "status": status,
            "alert": alert,
            "head": head_direction,
            "eyes": eyes_state,
            "yawn": yawn_state,
            "eye_closed_time": eye_closed_time,
            "head_off_road_time": head_off_road_time,
            "yawn_count": yawn_count_window,
            "calibrating": not self.calibration.finished,
            "calibration_remaining": calibration_remaining
        }