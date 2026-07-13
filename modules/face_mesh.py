import cv2
import mediapipe as mp


class FaceMeshDetector:

    def __init__(self):

        self.mp_face_mesh = mp.solutions.face_mesh

        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        self.mp_draw = mp.solutions.drawing_utils

    def process(self, frame):

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        results = self.face_mesh.process(rgb)

        return results

    def draw(
        self,
        frame,
        results
    ):

        if not results.multi_face_landmarks:
            return frame

        for face_landmarks in results.multi_face_landmarks:

            self.mp_draw.draw_landmarks(
                image=frame,
                landmark_list=face_landmarks,
                connections=self.mp_face_mesh.FACEMESH_TESSELATION,

                landmark_drawing_spec=self.mp_draw.DrawingSpec(
                    color=(140, 140, 140),
                    thickness=1,
                    circle_radius=1
                ),

                connection_drawing_spec=self.mp_draw.DrawingSpec(
                    color=(45, 45, 45),
                    thickness=1,
                    circle_radius=0
                )
            )

        return frame
    

