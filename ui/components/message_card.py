from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QHBoxLayout
)

from PySide6.QtCore import Qt


class MessageCard(QFrame):

    def __init__(self):
        super().__init__()

        self.setObjectName("card")

        self.build_ui()

    def build_ui(self):

        layout = QHBoxLayout(self)

        layout.setContentsMargins(
            18,
            18,
            18,
            18
        )

        layout.setSpacing(18)

        # -----------------------------
        # Icon
        # -----------------------------

        self.icon = QLabel("💬")

        self.icon.setFixedSize(
            38,
            38
        )

        self.icon.setAlignment(
            Qt.AlignCenter
        )

        self.icon.setStyleSheet("""
            QLabel{
                background:#12351f;
                color:#57f04f;
                border-radius:10px;
                font-size:20px;
                font-weight:900;
            }
        """)

        # -----------------------------
        # Text
        # -----------------------------

        text_layout = QVBoxLayout()

        text_layout.setSpacing(6)

        self.title = QLabel(
            "Driver behavior is normal."
        )

        self.title.setObjectName(
            "messageTitle"
        )

        self.subtitle = QLabel(
            "No signs of fatigue or distraction."
        )

        self.subtitle.setObjectName(
            "messageSub"
        )

        self.subtitle.setWordWrap(
            True
        )

        text_layout.addStretch()
        text_layout.addWidget(
            self.title
        )
        text_layout.addWidget(
            self.subtitle
        )
        text_layout.addStretch()

        layout.addWidget(
            self.icon
        )

        layout.addLayout(
            text_layout
        )

    # ======================================================

    def update_message(
        self,
        status
    ):

        if status == "NORMAL":

            self.icon.setText("💬")

            self.icon.setStyleSheet("""
                QLabel{
                    background:#12351f;
                    color:#57f04f;
                    border-radius:10px;
                    font-size:28px;
                    font-weight:900;
                }
            """)

            self.title.setText(
                "Driver behavior is normal."
            )

            self.subtitle.setText(
                "No signs of fatigue or distraction."
            )

        elif status == "WARNING":

            self.icon.setText("⚠️")

            self.icon.setStyleSheet("""
                QLabel{
                    background:#3b2e07;
                    color:#facc15;
                    border-radius:10px;
                    font-size:28px;
                    font-weight:900;
                }
            """)

            self.title.setText(
                "Driver attention warning."
            )

            self.subtitle.setText(
                "Driver is looking away from the road or showing abnormal behavior."
            )

        elif status == "DROWSY":

            self.icon.setText("🚨")

            self.icon.setStyleSheet("""
                QLabel{
                    background:#3b0a0a;
                    color:#ef4444;
                    border-radius:10px;
                    font-size:28px;
                    font-weight:900;
                }
            """)

            self.title.setText(
                "Drowsiness detected."
            )

            self.subtitle.setText(
                "Immediate attention is required. Please stop driving safely."
            )