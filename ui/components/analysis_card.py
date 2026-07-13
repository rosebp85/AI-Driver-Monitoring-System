from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QHBoxLayout
)

from PySide6.QtCore import Qt


class AnalysisCard(QFrame):

    def __init__(self):
        super().__init__()

        self.setObjectName("analysisCard")

        self.build_ui()

    def build_ui(self):

        layout = QHBoxLayout(self)

        layout.setContentsMargins(
            16,
            12,
            16,
            12
        )

        layout.setSpacing(14)

        self.icon_label = QLabel("🧠")

        self.icon_label.setAlignment(
            Qt.AlignCenter
        )

        self.icon_label.setStyleSheet("""
            QLabel {
                font-size: 30px;
                background: transparent;
                border: none;
            }
        """)

        self.text_label = QLabel(
            "Driver is maintaining good attention.\n"
            "All indicators are within safe limits.\n"
            "Keep up the good driving!"
        )

        self.text_label.setObjectName(
            "analysisText"
        )

        self.text_label.setWordWrap(
            True
        )

        layout.addWidget(
            self.icon_label,
            stretch=1
        )

        layout.addWidget(
            self.text_label,
            stretch=6
        )

    def update_analysis(
        self,
        status
    ):

        if status == "NORMAL":

            self.text_label.setText(
                "Driver is maintaining good attention.\n"
                "All indicators are within safe limits.\n"
                "Keep up the good driving!"
            )

        elif status == "WARNING":

            self.text_label.setText(
                "Driver shows signs of distraction.\n"
                "Please keep your head and eyes toward the road."
            )

        elif status == "DROWSY":

            self.text_label.setText(
                "Fatigue risk is high.\n"
                "Prolonged eye closure or drowsy behavior detected."
            )