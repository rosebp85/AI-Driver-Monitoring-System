from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy
)

from PySide6.QtCore import Qt

from ui.video_widget import VideoWidget
from ui.side_panel import SidePanel


class Dashboard(QFrame):

    def __init__(self):
        super().__init__()

        self.setObjectName("appFrame")

        self.build_ui()

    def build_ui(self):

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(18)

        # -----------------------------
        # Header
        # -----------------------------

        header = QFrame()
        header.setObjectName("topBar")

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 14)
        header_layout.setSpacing(14)

        logo = QLabel("◎")
        logo.setObjectName("logo")
        logo.setFixedSize(48, 48)
        logo.setAlignment(Qt.AlignCenter)

        title_layout = QVBoxLayout()
        title_layout.setSpacing(3)

        title = QLabel(
            '<span style="color:#2f8cff;">AI DRIVER</span> MONITORING SYSTEM'
        )
        title.setObjectName("title")

        subtitle = QLabel(
            "Camera-based driver behavior analysis"
        )
        subtitle.setObjectName("subtitle")

        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)

        active = QLabel("● SYSTEM ACTIVE")
        active.setObjectName("systemActive")
        active.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        header_layout.addWidget(logo)
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        header_layout.addWidget(active)

        root.addWidget(header, stretch=1)

        # -----------------------------
        # Body
        # -----------------------------

        body = QHBoxLayout()
        body.setSpacing(18)

        self.video_widget = VideoWidget()
        self.side_panel = SidePanel()

        self.video_widget.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        self.side_panel.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        body.addWidget(self.video_widget, stretch=6)
        body.addWidget(self.side_panel, stretch=4)

        root.addLayout(body, stretch=12)

    """    # -----------------------------
        # Bottom Strip
        # -----------------------------

        bottom = QFrame()
        bottom.setObjectName("bottomStrip")

        bottom_layout = QHBoxLayout(bottom)
        bottom_layout.setContentsMargins(18, 10, 18, 10)
        bottom_layout.setSpacing(18)

        bottom_layout.addWidget(
            self.bottom_item(
                "🛡️",
                "Safe Drive, Save Life",
                "Your safety is our priority."
            )
        )

        bottom_layout.addWidget(
            self.bottom_item(
                "⚠️",
                "Audio Alert",
                "DROWSY state only"
            )
        )

        bottom_layout.addWidget(
            self.bottom_item(
                "◎",
                "Calibration",
                "Initializing system"
            )
        )

        bottom_layout.addWidget(
            self.bottom_item(
                "⌘",
                "Built with",
                "Python · OpenCV · MediaPipe · PySide6"
            )
        )

        root.addWidget(bottom, stretch=1)
"""
    def bottom_item(
        self,
        icon_text,
        title_text,
        subtitle_text
    ):

        item = QFrame()

        layout = QHBoxLayout(item)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        icon = QLabel(icon_text)
        icon.setAlignment(Qt.AlignCenter)
        icon.setStyleSheet("""
            QLabel {
                font-size: 26px;
                background: transparent;
                border: none;
            }
        """)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)

        title = QLabel(title_text)
        title.setObjectName("bottomTitle")

        subtitle = QLabel(subtitle_text)
        subtitle.setObjectName("bottomSub")
        subtitle.setWordWrap(True)

        text_layout.addStretch()
        text_layout.addWidget(title)
        text_layout.addWidget(subtitle)
        text_layout.addStretch()

        layout.addWidget(icon)
        layout.addLayout(text_layout)

        return item