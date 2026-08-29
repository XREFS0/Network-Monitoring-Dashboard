from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QFrame
from PySide6.QtCore import Qt
from ..widgets.metric_card import MetricCard
from ..widgets.traffic_chart import TrafficChart
from ...utils.formatting import format_bytes, format_speed
from ...core.models import NetworkOverview, SystemStats

class DashboardView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)

        self.cards_layout = QGridLayout()
        self.cards_layout.setSpacing(15)

        self.card_dl = MetricCard("DOWNLOAD SPEED")
        self.card_ul = MetricCard("UPLOAD SPEED")
        self.card_total_dl = MetricCard("TOTAL RECEIVED")
        self.card_total_ul = MetricCard("TOTAL SENT")

        self.cards_layout.addWidget(self.card_dl, 0, 0)
        self.cards_layout.addWidget(self.card_ul, 0, 1)
        self.cards_layout.addWidget(self.card_total_dl, 0, 2)
        self.cards_layout.addWidget(self.card_total_ul, 0, 3)

        self.layout.addLayout(self.cards_layout)

        self.chart_frame = QFrame()
        self.chart_frame.setObjectName("Card")
        self.chart_layout = QVBoxLayout(self.chart_frame)
        self.chart_layout.setContentsMargins(12, 12, 12, 12)

        self.chart_title = QLabel("REAL-TIME TRAFFIC (ROLLING)")
        self.chart_title.setObjectName("CardTitle")
        self.chart_layout.addWidget(self.chart_title)

        self.chart = TrafficChart()
        self.chart.setMinimumHeight(250)
        self.chart_layout.addWidget(self.chart)

        self.layout.addWidget(self.chart_frame)

        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.setSpacing(20)

        self.sys_frame = QFrame()
        self.sys_frame.setObjectName("Card")
        self.sys_layout = QVBoxLayout(self.sys_frame)
        self.sys_layout.setContentsMargins(16, 16, 16, 16)
        self.sys_layout.setSpacing(10)

        sys_title = QLabel("SYSTEM & CONTEXT")
        sys_title.setObjectName("CardTitle")
        self.sys_layout.addWidget(sys_title)

        self.lbl_cpu = QLabel("CPU Usage: --")
        self.lbl_mem = QLabel("Memory Usage: --")
        self.lbl_host = QLabel("Hostname: --")
        self.lbl_plat = QLabel("Platform: --")

        self.sys_layout.addWidget(self.lbl_cpu)
        self.sys_layout.addWidget(self.lbl_mem)
        self.sys_layout.addWidget(self.lbl_host)
        self.sys_layout.addWidget(self.lbl_plat)
        self.sys_layout.addStretch()

        self.bottom_layout.addWidget(self.sys_frame, 1)

        self.info_frame = QFrame()
        self.info_frame.setObjectName("Card")
        self.info_layout = QVBoxLayout(self.info_frame)
        self.info_layout.setContentsMargins(16, 16, 16, 16)
        self.info_layout.setSpacing(10)

        info_title = QLabel("CONNECTION STATUS")
        info_title.setObjectName("CardTitle")
        self.info_layout.addWidget(info_title)

        self.lbl_active_if = QLabel("Active Interface: --")
        self.lbl_status = QLabel("Status: --")
        self.lbl_ip = QLabel("IP Address: --")
        self.lbl_mac = QLabel("MAC Address: --")

        self.info_layout.addWidget(self.lbl_active_if)
        self.info_layout.addWidget(self.lbl_status)
        self.info_layout.addWidget(self.lbl_ip)
        self.info_layout.addWidget(self.lbl_mac)
        self.info_layout.addStretch()

        self.bottom_layout.addWidget(self.info_frame, 1)

        self.layout.addLayout(self.bottom_layout)

    def update_theme(self, is_dark: bool):
        self.chart.set_theme(is_dark)

    def update_data(self, overview: NetworkOverview, sys_stats: SystemStats):
        dl_fmt = format_speed(overview.bytes_recv_speed).split()
        ul_fmt = format_speed(overview.bytes_sent_speed).split()

        self.card_dl.update_value(dl_fmt[0], dl_fmt[1])
        self.card_ul.update_value(ul_fmt[0], ul_fmt[1])

        tot_dl_fmt = format_bytes(overview.total_bytes_recv).split()
        tot_ul_fmt = format_bytes(overview.total_bytes_sent).split()

        self.card_total_dl.update_value(tot_dl_fmt[0], tot_dl_fmt[1])
        self.card_total_ul.update_value(tot_ul_fmt[0], tot_ul_fmt[1])

        self.chart.add_sample(overview.bytes_recv_speed, overview.bytes_sent_speed)

        self.lbl_cpu.setText(f"CPU Usage: {sys_stats.cpu_usage:.1f}%")
        self.lbl_mem.setText(f"Memory Usage: {sys_stats.memory_usage:.1f}%")
        self.lbl_host.setText(f"Hostname: {sys_stats.hostname}")
        self.lbl_plat.setText(f"Platform: {sys_stats.platform_name}")

        active_if = overview.active_interface if overview.active_interface else "None detected"
        self.lbl_active_if.setText(f"Active Interface: {active_if}")
        self.lbl_status.setText(f"Status: {overview.connection_status}")
        self.lbl_ip.setText(f"IP Address: {overview.current_ip if overview.current_ip else 'N/A'}")
        self.lbl_mac.setText(f"MAC Address: {overview.mac_address if overview.mac_address else 'N/A'}")
