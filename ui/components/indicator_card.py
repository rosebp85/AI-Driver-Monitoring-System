from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout
)

from PySide6.QtCore import Qt


class IndicatorCard(QFrame):

    def __init__(
        self,
        title,
        icon,
        value
    ):
        super().__init__()

        self.setObjectName("card")

        self.title_text = title
        self.icon_text = icon
        self.value_text = value

        self.build_ui()

    def build_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            10,
            10,
            10,
            10
        )

        layout.setSpacing(6)

        self.title_label = QLabel(
            self.title_text
        )

        self.title_label.setObjectName(
            "smallTitle"
        )

        self.title_label.setAlignment(
            Qt.AlignCenter
        )

        self.icon_label = QLabel(
            self.icon_text
        )

        self.icon_label.setObjectName(
            "smallIcon"
        )

        self.icon_label.setAlignment(
            Qt.AlignCenter
        )

        self.value_label = QLabel(
            self.value_text
        )

        self.value_label.setObjectName(
            "smallValue"
        )

        self.value_label.setAlignment(
            Qt.AlignCenter
        )

        layout.addStretch()
        layout.addWidget(self.title_label)
        layout.addWidget(self.icon_label)
        layout.addWidget(self.value_label)
        layout.addStretch()

    def update_value(
        self,
        value
    ):

        self.value_label.setText(
            value
        )