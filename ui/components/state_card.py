from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QHBoxLayout
)

from PySide6.QtCore import Qt


class StateCard(QFrame):

    def __init__(self):
        super().__init__()

        self.setObjectName("stateCard")

        self.build_ui()

    def build_ui(self):

        layout = QHBoxLayout(self)

        layout.setContentsMargins(
            24,
            16,
            24,
            16
        )

        layout.setSpacing(20)

        self.icon_label = QLabel("🛡️")

        self.icon_label.setAlignment(
            Qt.AlignCenter
        )

        self.icon_label.setStyleSheet("""
            QLabel {
                font-size: 42px;
                background: transparent;
                border: none;
            }
        """)

        text_layout = QVBoxLayout()

        text_layout.setSpacing(4)

        self.state_label = QLabel(
            "NORMAL"
        )

        self.state_label.setObjectName(
            "stateText"
        )

        self.state_label.setAlignment(
            Qt.AlignLeft
        )

        self.subtitle_label = QLabel(
            "Driver is focused and attentive"
        )

        self.subtitle_label.setObjectName(
            "stateSubText"
        )

        self.subtitle_label.setAlignment(
            Qt.AlignLeft
        )

        text_layout.addStretch()
        text_layout.addWidget(
            self.state_label
        )
        text_layout.addWidget(
            self.subtitle_label
        )
        text_layout.addStretch()

        layout.addWidget(
            self.icon_label,
            stretch=1
        )

        layout.addLayout(
            text_layout,
            stretch=4
        )

    def update_state(
        self,
        status
    ):

        self.state_label.setText(
            status
        )

        if status == "NORMAL":

            self.icon_label.setText(
                "🛡️"
            )

            self.subtitle_label.setText(
                "Driver is focused and attentive"
            )

            self.setStyleSheet("""
                QFrame#stateCard {
                    background-color: #052e16;
                    border: 1px solid #57f04f;
                    border-radius: 16px;
                }

                QLabel#stateText {
                    color: #57f04f;
                }
            """)

        elif status == "WARNING":

            self.icon_label.setText(
                "⚠️"
            )

            self.subtitle_label.setText(
                "Driver attention warning"
            )

            self.setStyleSheet("""
                QFrame#stateCard {
                    background-color: #2e2405;
                    border: 1px solid #facc15;
                    border-radius: 16px;
                }

                QLabel#stateText {
                    color: #facc15;
                }
            """)

        elif status == "DROWSY":

            self.icon_label.setText(
                "🚨"
            )

            self.subtitle_label.setText(
                "Drowsiness risk detected"
            )

            self.setStyleSheet("""
                QFrame#stateCard {
                    background-color: #2e0505;
                    border: 1px solid #ef4444;
                    border-radius: 16px;
                }

                QLabel#stateText {
                    color: #ef4444;
                }
            """)