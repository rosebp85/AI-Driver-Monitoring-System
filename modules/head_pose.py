import cv2
import numpy as np
import math


class HeadPoseEstimator:

    def __init__(self):

        self.landmark_ids = {
            "nose_tip": 1,
            "chin": 152,
            "left_eye": 33,
            "right_eye": 263,
            "mouth_left": 61,
            "mouth_right": 291
        }
        self.face_model_3d = np.array([
            (0.0,   0.0,    0.0),      # Nose Tip
            (0.0, -63.6, -12.5),       # Chin
            (-43.3, 32.7, -26.0),      # Left Eye Corner
            (43.3, 32.7, -26.0),       # Right Eye Corner
            (-28.9,-28.9,-24.1),       # Left Mouth Corner
            (28.9,-28.9,-24.1)         # Right Mouth Corner
        ], dtype=np.float64)

    def get_face_points(
        self,
        face_landmarks,
        img_w,
        img_h
    ):

        points = {}

        for name, idx in self.landmark_ids.items():

            landmark = face_landmarks.landmark[idx]

            x = int(
                landmark.x * img_w
            )

            y = int(
                landmark.y * img_h
            )

            points[name] = (x, y)

        return points
    
    def estimate_pose(
        self,
        face_landmarks,
        img_w,
        img_h
    ):

        # -----------------------------
        # استخراج نقاط دوبعدی صورت
        # -----------------------------

        face_2d = []

        for idx in self.landmark_ids.values():

            landmark = face_landmarks.landmark[idx]

            x = landmark.x * img_w
            y = landmark.y * img_h

            face_2d.append([x, y])

        face_2d = np.array(
            face_2d,
            dtype=np.float64
        )

        # -----------------------------
        # Camera Matrix
        # -----------------------------

        focal_length = img_w

        camera_matrix = np.array([
            [focal_length, 0, img_w / 2],
            [0, focal_length, img_h / 2],
            [0, 0, 1]
        ], dtype=np.float64)

        # -----------------------------
        # Distortion Matrix
        # -----------------------------

        dist_matrix = np.zeros(
            (4, 1),
            dtype=np.float64
        )

        # -----------------------------
        # Solve PnP
        # -----------------------------

        success, rotation_vector, translation_vector = cv2.solvePnP(
            self.face_model_3d,
            face_2d,
            camera_matrix,
            dist_matrix
        )

        # -----------------------------
        # Rotation Matrix
        # -----------------------------

        rotation_matrix, _ = cv2.Rodrigues(
            rotation_vector
        )

        sy = math.sqrt(
            rotation_matrix[0, 0] ** 2 +
            rotation_matrix[1, 0] ** 2
        )

        singular = sy < 1e-6

        if not singular:

            pitch = math.atan2(
                rotation_matrix[2, 1],
                rotation_matrix[2, 2]
            )

            yaw = math.atan2(
                -rotation_matrix[2, 0],
                sy
            )

            roll = math.atan2(
                rotation_matrix[1, 0],
                rotation_matrix[0, 0]
            )

        else:

            pitch = math.atan2(
                -rotation_matrix[1, 2],
                rotation_matrix[1, 1]
            )

            yaw = math.atan2(
                -rotation_matrix[2, 0],
                sy
            )

            roll = 0

        pitch = math.degrees(pitch)
        yaw = math.degrees(yaw)
        roll = math.degrees(roll)


        return (
            success,
            yaw,
            pitch,
            roll,
            rotation_vector,
            rotation_matrix,
            translation_vector,
            camera_matrix,
            dist_matrix
        )
    
    def get_direction(
        self,
        rotation_matrix
    ):

        z_axis = rotation_matrix[:, 2]

        x = z_axis[0]
        y = z_axis[1]
        z = z_axis[2]

        return (
            x,
            y,
            z
        )


    
    def draw_axes(
        self,
        frame,
        nose_point,
        rotation_vector,
        translation_vector,
        camera_matrix,
        dist_matrix
    ):
            
        axis_3d = np.float32([
            [50, 0, 0],     # محور X
            [0, 50, 0],     # محور Y
            [0, 0, 50]      # محور Z
        ]).reshape(-1, 3)

        axis_2d, _ = cv2.projectPoints(
            axis_3d,
            rotation_vector,
            translation_vector,
            camera_matrix,
            dist_matrix
        )

        axis_2d = axis_2d.reshape(-1, 2)

        x_axis = tuple(axis_2d[0].astype(int))
        y_axis = tuple(axis_2d[1].astype(int))
        z_axis = tuple(axis_2d[2].astype(int))
        
        nose_point = tuple(map(int, nose_point))

        cv2.line(
            frame,
            nose_point,
            x_axis,
            (0, 0, 255),
            3
        )

        cv2.line(
            frame,
            nose_point,
            y_axis,
            (0, 255, 0),
            3
        )

        cv2.line(
            frame,
            nose_point,
            z_axis,
            (255, 0, 0),
            3
        )

        return frame
