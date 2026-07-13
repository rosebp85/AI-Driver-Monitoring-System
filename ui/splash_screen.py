from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QProgressBar
from PySide6.QtCore import Qt


class SplashScreen(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
        )

        self.setFixedSize(520, 300)

        self.setStyleSheet("""
            QWidget {
                background-color: #020713;
                color: #e5e7eb;
                border: 1px solid #18304a;
                border-radius: 20px;
                font-family: Segoe UI;
            }

            QLabel#title {
                font-size: 28px;
                font-weight: 900;
                color: #2f8cff;
            }

            QLabel#subtitle {
                font-size: 14px;
                color: #94a3b8;
            }

            QProgressBar {
                border: 1px solid #243b57;
                border-radius: 8px;
                background-color: #071022;
                height: 14px;
            }

            QProgressBar::chunk {
                background-color: #57f04f;
                border-radius: 8px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(18)

        title = QLabel("AI DRIVER MONITORING")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Initializing vision system...")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(False)

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.progress)
        layout.addStretch()