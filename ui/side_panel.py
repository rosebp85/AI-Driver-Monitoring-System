from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QGridLayout,
    QSizePolicy
)

from ui.components.state_card import StateCard
from ui.components.message_card import MessageCard
from ui.components.indicator_card import IndicatorCard
from ui.components.metric_card import MetricCard
from ui.components.analysis_card import AnalysisCard


class SidePanel(QFrame):

    def __init__(self):
        super().__init__()

        self.setObjectName("sidePanel")

        self.build_ui()

    # ======================================================

    def build_ui(self):

        root = QVBoxLayout(self)

        root.setContentsMargins(
            18,
            18,
            18,
            18
        )

        root.setSpacing(8)

        # --------------------------------------------------

        root.addWidget(
            self.section_title(
                "FINAL DRIVER STATE"
            )
        )

        self.state_card = StateCard()

        self.state_card.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        root.addWidget(
            self.state_card,
            stretch=3
        )

        # --------------------------------------------------

        root.addWidget(
            self.section_title(
                "MAIN MESSAGE"
            )
        )

        self.message_card = MessageCard()

        self.message_card.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        root.addWidget(
            self.message_card,
            stretch=2
        )

        # --------------------------------------------------

        root.addWidget(
            self.section_title(
                "KEY INDICATORS"
            )
        )

        indicators = QGridLayout()

        indicators.setHorizontalSpacing(10)
        indicators.setVerticalSpacing(10)

        self.eye_card = IndicatorCard(
            "EYES",
            "👁",
            "OPEN"
        )

        self.head_card = IndicatorCard(
            "HEAD",
            "👤",
            "CENTER"
        )

        self.yawn_card = IndicatorCard(
            "YAWN",
            "🥱",
            "NO"
        )

        indicators.addWidget(
            self.eye_card,
            0,
            0
        )

        indicators.addWidget(
            self.head_card,
            0,
            1
        )

        indicators.addWidget(
            self.yawn_card,
            0,
            2
        )

        root.addLayout(
            indicators,
            stretch=2
        )

        # --------------------------------------------------

        root.addWidget(
            self.section_title(
                "BEHAVIOR METRICS"
            )
        )

        metrics = QGridLayout()

        metrics.setHorizontalSpacing(10)
        metrics.setVerticalSpacing(10)

        self.eye_time = MetricCard(
            "EYE CLOSED",
            "0.00 s"
        )

        self.head_time = MetricCard(
            "HEAD OFF ROAD",
            "0.00 s"
        )

        self.yawns = MetricCard(
            "YAWNS",
            "0"
        )

        metrics.addWidget(
            self.eye_time,
            0,
            0
        )

        metrics.addWidget(
            self.head_time,
            0,
            1
        )

        metrics.addWidget(
            self.yawns,
            0,
            2
        )

        root.addLayout(
            metrics,
            stretch=1
        )

        # --------------------------------------------------

        root.addWidget(
            self.section_title(
                "BEHAVIOR ANALYSIS"
            )
        )

        self.analysis = AnalysisCard()

        self.analysis.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        root.addWidget(
            self.analysis,
            stretch=2
        )

    # ======================================================

    def section_title(
        self,
        text
    ):

        label = QLabel(text)

        label.setObjectName(
            "sectionTitle"
        )

        return label

    # ======================================================

    def update(
        self,
        status,
        head,
        eyes,
        yawn,
        eye_closed_time,
        head_off_road_time,
        yawn_count
    ):

        self.state_card.update_state(
            status
        )

        self.message_card.update_message(
            status
        )

        self.analysis.update_analysis(
            status
        )

        self.eye_card.update_value(
            eyes
        )

        self.head_card.update_value(
            head
        )

        self.yawn_card.update_value(
            yawn
        )

        self.eye_time.update_value(
            eye_closed_time
        )

        self.head_time.update_value(
            head_off_road_time
        )

        self.yawns.update_value(
            yawn_count
        )