
"""
Debug Version

This file is kept for development and debugging only.

Run the application using:

    python app.py
"""



import cv2

from modules.face_mesh import FaceMeshDetector
from modules.head_pose import HeadPoseEstimator
from modules.head_direction import HeadDirectionClassifier
from modules.calibration import HeadCalibration
from modules.eye_tracker import EyeTracker
from modules.yawn_detector import YawnDetector
from modules.driver_behavior import DriverBehavior

cam = cv2.VideoCapture(0)

mesh_detector = FaceMeshDetector()
head_pose = HeadPoseEstimator()
direction = HeadDirectionClassifier()
calibration = HeadCalibration()
eye_tracker = EyeTracker()
yawn_detector = YawnDetector()
driver_behavior = DriverBehavior()


while True:

    ret, img = cam.read()

    if not ret:
        break

    img = cv2.flip(img, 1)
    status = "CALIBRATING"
    drowsiness_score = 0
    alert = None

    results = mesh_detector.process(img)

    if results.multi_face_landmarks:

        face_landmarks = results.multi_face_landmarks[0]

        h, w, _ = img.shape

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
        ) = head_pose.estimate_pose(
            face_landmarks,
            w,
            h
        )

        if success:

            calibration.update(
                yaw,
                pitch
            )

            if calibration.finished:

                yaw, pitch = calibration.normalize(
                    yaw,
                    pitch
                )

                if pitch > 180:
                    pitch -= 360

                if yaw > 180:
                    yaw -= 360

                head_direction = direction.classify(
                    yaw,
                    pitch
                )

                ear = eye_tracker.get_ear(
                    face_landmarks
                )

                closed = eye_tracker.is_closed(
                    ear
                )

                blink_count = eye_tracker.update_blink(
                    closed
                )

                is_drowsy, closed_duration = eye_tracker.detect_drowsiness(
                    closed
                )

                mar, mouth_open, is_yawning, yawn_count = yawn_detector.detect(
                    face_landmarks
                )

                behavior = driver_behavior.update(
                    closed,
                    head_direction,
                    is_yawning
                )

                status = behavior["status"]
                alert = behavior["alert"]
                eye_closed_time = behavior["eye_closed_time"]
                head_off_road_time = behavior["head_off_road_time"]
                yawn_count_window = behavior["yawn_count"]

                

                print(
                    f"Direction={head_direction} | "
                    f"EAR={ear:.3f} | "
                    f"EyesClosed={closed} | "
                    f"Blinks={blink_count} | "
                    f"MAR={mar:.3f} | "
                    f"Yawning={is_yawning} | "
                    f"EyeClosedTime={eye_closed_time:.2f}s | "
                    f"HeadOffRoadTime={head_off_road_time:.2f}s | "
                    f"YawnsInWindow={yawn_count_window} | "
                    f"Status={status} | "
                    f"Alert={alert}"
                )
                



            nose_point = (
                int(face_landmarks.landmark[1].x * w),
                int(face_landmarks.landmark[1].y * h)
            )

            img = head_pose.draw_axes(
                img,
                nose_point,
                rotation_vector,
                translation_vector,
                camera_matrix,
                dist_matrix
            )

    img = mesh_detector.draw(
        img,
        results
    )

    cv2.imshow(
        "Driver Monitoring",
        img
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cam.release()
cv2.destroyAllWindows()