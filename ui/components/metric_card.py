from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout
)

from PySide6.QtCore import Qt


class MetricCard(QFrame):

    def __init__(
        self,
        title,
        value
    ):
        super().__init__()

        self.setObjectName("card")

        self.title_text = title
        self.value_text = value

        self.build_ui()

    # --------------------------------------------------

    def build_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            10,
            8,
            10,
            8
        )

        layout.setSpacing(4)

        self.title_label = QLabel(
            self.title_text
        )

        self.title_label.setObjectName(
            "metricTitle"
        )

        self.title_label.setAlignment(
            Qt.AlignCenter
        )

        self.value_label = QLabel(
            self.value_text
        )

        self.value_label.setObjectName(
            "metricValue"
        )

        self.value_label.setAlignment(
            Qt.AlignCenter
        )

        layout.addStretch()

        layout.addWidget(
            self.title_label
        )

        layout.addWidget(
            self.value_label
        )

        layout.addStretch()

    # --------------------------------------------------

    def update_value(
        self,
        value
    ):

        if isinstance(
            value,
            float
        ):

            self.value_label.setText(
                f"{value:.2f}"
            )

        else:

            self.value_label.setText(
                str(value)
            )