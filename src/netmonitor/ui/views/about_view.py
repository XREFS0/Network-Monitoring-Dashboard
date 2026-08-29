from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt

class AboutView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)

        self.title_label = QLabel("ABOUT")
        self.title_label.setObjectName("CardTitle")
        self.layout.addWidget(self.title_label)

        self.card = QFrame()
        self.card.setObjectName("Card")
        self.card_layout = QVBoxLayout(self.card)
        self.card_layout.setContentsMargins(24, 24, 24, 24)
        self.card_layout.setSpacing(12)

        name_lbl = QLabel("Network Monitoring Dashboard")
        name_lbl.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.card_layout.addWidget(name_lbl)

        ver_lbl = QLabel("Version: 1.0.0")
        ver_lbl.setStyleSheet("color: #94a3b8;")
        self.card_layout.addWidget(ver_lbl)

        desc_lbl = QLabel(
            "A professional-grade, cross-platform local network and system resource monitoring "
            "dashboard written in Python and PySide6."
        )
        desc_lbl.setWordWrap(True)
        self.card_layout.addWidget(desc_lbl)

        tech_title = QLabel("Technology Stack:")
        tech_title.setStyleSheet("font-weight: bold; margin-top: 10px;")
        self.card_layout.addWidget(tech_title)

        tech_lbl = QLabel(
            "• Python 3.12+\n"
            "• PySide6 (Qt for Python)\n"
            "• psutil (Process and System Utilities)\n"
            "• Custom QPainter-based high-performance graphing engine"
        )
        self.card_layout.addWidget(tech_lbl)

        copyright_title = QLabel("Copyright:")
        copyright_title.setStyleSheet("font-weight: bold; margin-top: 10px;")
        self.card_layout.addWidget(copyright_title)

        copyright_lbl = QLabel("© 2026 XREFS0. All Rights Reserved.")
        self.card_layout.addWidget(copyright_lbl)

        links_title = QLabel("Developer Links:")
        links_title.setStyleSheet("font-weight: bold; margin-top: 10px;")
        self.card_layout.addWidget(links_title)

        links_lbl = QLabel(
            '• Facebook page: <a href="https://www.facebook.com/XREFS0" style="color: #3b82f6; text-decoration: none;">Click</a><br>'
            '• Contact via Telegram: <a href="https://t.me/MrMasaOfficial" style="color: #3b82f6; text-decoration: none;">Click</a><br>'
            '• Telegram Channel: <a href="https://t.me/XREFS0_CHANNEL" style="color: #3b82f6; text-decoration: none;">Click</a><br>'
            '• Website: <a href="http://xrefs0.com/" style="color: #3b82f6; text-decoration: none;">Click</a><br>'
            '• YouTube: <a href="https://www.youtube.com/@XREFS0" style="color: #3b82f6; text-decoration: none;">Click</a>'
        )
        links_lbl.setOpenExternalLinks(True)
        self.card_layout.addWidget(links_lbl)

        self.card_layout.addStretch()
        self.layout.addWidget(self.card)
        self.layout.addStretch()
