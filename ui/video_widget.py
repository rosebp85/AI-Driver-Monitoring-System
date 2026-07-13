from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QWidget
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


class VideoWidget(QFrame):

    def __init__(self):
        super().__init__()

        self.setObjectName("videoFrame")
        self.build_ui()

    def build_ui(self):

        root = QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(12)

        header = QHBoxLayout()

        title = QLabel("LIVE CAMERA FEED")
        title.setObjectName("sectionTitle")

        header.addWidget(title)
        header.addStretch()

        root.addLayout(header)

        self.video_container = QWidget()
        self.video_container.setStyleSheet("""
            QWidget {
                background-color: #020617;
                border-radius: 16px;
            }
        """)

        self.video_label = QLabel(self.video_container)
        self.video_label.setObjectName("videoLabel")
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setText("Camera Preview")

        self.live_badge = QLabel("● LIVE", self.video_container)
        self.live_badge.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 180);
                color: white;
                border-radius: 10px;
                padding: 7px 14px;
                font-size: 12px;
                font-weight: 900;
            }
        """)

        self.fps_badge = QLabel("⌁ FPS: --", self.video_container)
        self.fps_badge.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 160);
                color: #57f04f;
                border-radius: 10px;
                padding: 7px 14px;
                font-size: 12px;
                font-weight: 900;
            }
        """)

        self.calibration_box = QLabel("CALIBRATION\n\n3", self.video_container)
        self.calibration_box.setAlignment(Qt.AlignCenter)
        self.calibration_box.setStyleSheet("""
            QLabel {
                background-color: rgba(7, 16, 34, 210);
                color: white;
                border: 1px solid #243b57;
                border-radius: 18px;
                padding: 18px;
                font-size: 28px;
                font-weight: 900;
            }
        """)
        self.calibration_box.hide()

        root.addWidget(self.video_container, stretch=1)

    def resizeEvent(self, event):

        super().resizeEvent(event)

        w = self.video_container.width()
        h = self.video_container.height()

        self.video_label.setGeometry(
            0,
            0,
            w,
            h
        )

        self.live_badge.adjustSize()
        self.live_badge.move(
            22,
            22
        )

        self.fps_badge.adjustSize()
        self.fps_badge.move(
            22,
            h - self.fps_badge.height() - 22
        )

        box_w = 260
        box_h = 155

        self.calibration_box.setGeometry(
            int((w - box_w) / 2),
            int((h - box_h) * 0.72),
            box_w,
            box_h
        )

    def update_frame(self, pixmap: QPixmap):

        self.video_label.setPixmap(
            pixmap.scaled(
                self.video_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )

    def update_fps(self, fps):

        self.fps_badge.setText(
            f"⌁ FPS: {fps}"
        )

        self.fps_badge.adjustSize()

    def show_calibration(self, seconds):

        self.calibration_box.setText(
            f"CALIBRATION\n\n{seconds}"
        )

        self.calibration_box.show()

    def hide_calibration(self):

        self.calibration_box.hide()