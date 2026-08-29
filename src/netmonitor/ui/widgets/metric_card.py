from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt

class MetricCard(QFrame):
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.setObjectName("Card")
        self.setFrameShape(QFrame.StyledPanel)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(16, 16, 16, 16)
        self.layout.setSpacing(8)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("CardTitle")
        self.layout.addWidget(self.title_label)

        self.val_layout = QHBoxLayout()
        self.val_layout.setSpacing(4)

        self.value_label = QLabel("--")
        self.value_label.setObjectName("CardValue")
        self.val_layout.addWidget(self.value_label)

        self.unit_label = QLabel("")
        self.unit_label.setObjectName("CardUnit")
        self.unit_label.setAlignment(Qt.AlignBottom | Qt.AlignLeft)
        self.val_layout.addWidget(self.unit_label)
        self.val_layout.addStretch()

        self.layout.addLayout(self.val_layout)

    def update_value(self, value: str, unit: str = ""):
        self.value_label.setText(value)
        self.unit_label.setText(unit)
