import sys

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout
)

from PySide6.QtGui import (
    QGuiApplication,
    QPixmap
)

from ui.styles import APP_STYLE
from ui.dashboard import Dashboard
from ui.camera_worker import CameraWorker
from PySide6.QtCore import QTimer
from ui.splash_screen import SplashScreen


class DriverMonitoringApp(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "AI Driver Monitoring System"
        )

        self.setStyleSheet(
            APP_STYLE
        )

        self.resize_window()
        self.build_ui()
        self.start_camera()

    def resize_window(self):

        screen = QGuiApplication.primaryScreen()
        geometry = screen.availableGeometry()

        width = int(geometry.width() * 0.88)
        height = int(geometry.height() * 0.88)

        self.resize(width, height)
        self.setMinimumSize(1100, 680)

    def build_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            18,
            18,
            18,
            18
        )

        layout.setSpacing(0)

        self.dashboard = Dashboard()

        layout.addWidget(
            self.dashboard
        )

    def start_camera(self):

        self.camera_worker = CameraWorker()

        self.camera_worker.frame_ready.connect(
            self.update_video_frame
        )

        self.camera_worker.fps_ready.connect(
            self.dashboard.video_widget.update_fps
        )

        self.camera_worker.data_ready.connect(
            self.update_driver_data
        )

        self.camera_worker.start()

    def update_video_frame(self, q_image):

        pixmap = QPixmap.fromImage(q_image)

        self.dashboard.video_widget.update_frame(
            pixmap
        )

    def update_driver_data(self, data):

        self.dashboard.side_panel.update(
            data["status"],
            data["head"],
            data["eyes"],
            data["yawn"],
            data["eye_closed_time"],
            data["head_off_road_time"],
            data["yawn_count"]
        )

        if data["calibrating"]:
            self.dashboard.video_widget.show_calibration(
                data["calibration_remaining"]
            )
        else:
            self.dashboard.video_widget.hide_calibration()

    def closeEvent(self, event):

        if hasattr(self, "camera_worker"):
            self.camera_worker.stop()

        event.accept()


def run():

    app = QApplication(sys.argv)

    splash = SplashScreen()
    splash.show()

    progress_value = {"value": 0}

    def update_progress():

        progress_value["value"] += 5
        splash.progress.setValue(progress_value["value"])

        if progress_value["value"] >= 100:

            timer.stop()
            splash.close()

            window = DriverMonitoringApp()
            window.show()

            app.main_window = window

    timer = QTimer()
    timer.timeout.connect(update_progress)
    timer.start(60)

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":

    run()