import time
import cv2

from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QImage

from modules.driver_pipeline import DriverPipeline


class CameraWorker(QThread):

    frame_ready = Signal(QImage)
    fps_ready = Signal(int)
    data_ready = Signal(dict)

    def __init__(self):
        super().__init__()

        self.running = True
        self.pipeline = DriverPipeline()

    def run(self):

        cap = cv2.VideoCapture(0)

        prev_time = time.time()

        while self.running:

            ret, frame = cap.read()

            if not ret:
                continue

            frame = cv2.flip(frame, 1)

            data = self.pipeline.process(
                frame
            )

            processed_frame = data["frame"]

            rgb_frame = cv2.cvtColor(
                processed_frame,
                cv2.COLOR_BGR2RGB
            )

            h, w, ch = rgb_frame.shape

            q_image = QImage(
                rgb_frame.data,
                w,
                h,
                ch * w,
                QImage.Format_RGB888
            ).copy()

            self.frame_ready.emit(q_image)

            current_time = time.time()
            fps = int(
                1 / (current_time - prev_time)
            )
            prev_time = current_time

            self.fps_ready.emit(fps)

            self.data_ready.emit(data)

        cap.release()

    def stop(self):

        self.running = False
        self.quit()
        self.wait()