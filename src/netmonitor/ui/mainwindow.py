from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QStackedWidget, QLabel, QFrame, QMessageBox
from PySide6.QtCore import QThread, Slot, Qt
from ..core.config import AppConfig
from ..core.logger import setup_logger
from ..core.models import NetworkOverview, SystemStats
from ..monitoring.worker import MonitoringWorker
from .themes import get_theme_qss
from .views.dashboard_view import DashboardView
from .views.interfaces_view import InterfacesView
from .views.connections_view import ConnectionsView
from .views.statistics_view import StatisticsView
from .views.settings_view import SettingsView
from .views.about_view import AboutView

logger = setup_logger()

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Network Monitoring Dashboard")
        self.resize(1100, 700)

        self.config = AppConfig()
        
        self.thread = None
        self.worker = None

        self.init_ui()
        self.apply_theme()
        
        if self.config.start_automatically:
            self.start_monitoring()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(12, 20, 12, 20)
        sidebar_layout.setSpacing(8)

        title_lbl = QLabel("NETMONITOR")
        title_lbl.setStyleSheet("font-weight: 800; font-size: 16px; margin-bottom: 20px; padding-left: 10px; color: #3b82f6;")
        sidebar_layout.addWidget(title_lbl)

        self.nav_buttons = []
        views_info = [
            ("Dashboard", 0),
            ("Interfaces", 1),
            ("Connections", 2),
            ("Statistics", 3),
            ("Settings", 4),
            ("About", 5)
        ]

        for name, idx in views_info:
            btn = QPushButton(name)
            btn.setObjectName("SidebarButton")
            btn.setCheckable(True)
            btn.setAutoExclusive(True)
            btn.clicked.connect(lambda checked, i=idx: self.switch_view(i))
            sidebar_layout.addWidget(btn)
            self.nav_buttons.append(btn)

        self.nav_buttons[0].setChecked(True)

        sidebar_layout.addStretch()

        self.engine_status_lbl = QLabel("Monitoring: OFF")
        self.engine_status_lbl.setStyleSheet("font-weight: bold; color: #ef4444; padding-left: 10px;")
        sidebar_layout.addWidget(self.engine_status_lbl)

        self.btn_toggle_monitor = QPushButton("Start Monitor")
        self.btn_toggle_monitor.setObjectName("ToggleMonitorButton")
        self.btn_toggle_monitor.clicked.connect(self.toggle_monitoring)
        sidebar_layout.addWidget(self.btn_toggle_monitor)

        main_layout.addWidget(self.sidebar)

        self.view_container = QFrame()
        self.view_container.setObjectName("ViewContainer")
        view_container_layout = QVBoxLayout(self.view_container)
        view_container_layout.setContentsMargins(0, 0, 0, 0)

        self.stacked_widget = QStackedWidget()
        
        self.dashboard_view = DashboardView()
        self.interfaces_view = InterfacesView()
        self.connections_view = ConnectionsView()
        self.statistics_view = StatisticsView()
        self.settings_view = SettingsView(self.config)
        self.settings_view.config_changed.connect(self.on_config_changed)
        self.about_view = AboutView()

        self.stacked_widget.addWidget(self.dashboard_view)
        self.stacked_widget.addWidget(self.interfaces_view)
        self.stacked_widget.addWidget(self.connections_view)
        self.stacked_widget.addWidget(self.statistics_view)
        self.stacked_widget.addWidget(self.settings_view)
        self.stacked_widget.addWidget(self.about_view)

        view_container_layout.addWidget(self.stacked_widget)
        main_layout.addWidget(self.view_container, 1)

    def apply_theme(self):
        qss = get_theme_qss(self.config.theme)
        self.setStyleSheet(qss)
        self.dashboard_view.update_theme(self.config.theme == "dark")

    def switch_view(self, index: int):
        self.stacked_widget.setCurrentIndex(index)
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)

    def toggle_monitoring(self):
        if self.thread and self.thread.isRunning():
            self.stop_monitoring()
        else:
            self.start_monitoring()

    def start_monitoring(self):
        if self.thread and self.thread.isRunning():
            return

        self.thread = QThread()
        self.worker = MonitoringWorker(self.config.monitoring_interval, self.config.selected_interface)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.data_sampled.connect(self.on_data_sampled)
        self.worker.error_occurred.connect(self.on_error_occurred)

        self.thread.start()

        self.engine_status_lbl.setText("Monitoring: ON")
        self.engine_status_lbl.setStyleSheet("font-weight: bold; color: #10b981; padding-left: 10px;")
        self.btn_toggle_monitor.setText("Stop Monitor")

    def stop_monitoring(self):
        if not self.thread or not self.thread.isRunning():
            return

        self.worker.stop()
        self.thread.quit()
        self.thread.wait()

        self.thread = None
        self.worker = None

        self.engine_status_lbl.setText("Monitoring: OFF")
        self.engine_status_lbl.setStyleSheet("font-weight: bold; color: #ef4444; padding-left: 10px;")
        self.btn_toggle_monitor.setText("Start Monitor")

    @Slot(NetworkOverview, dict, list, SystemStats)
    def on_data_sampled(self, overview: NetworkOverview, interfaces: dict, connections: list, sys_stats: SystemStats):
        self.dashboard_view.update_data(overview, sys_stats)
        self.interfaces_view.update_data(interfaces)
        self.connections_view.update_data(connections)
        self.statistics_view.update_data(interfaces)
        
        self.settings_view.update_interfaces(list(interfaces.keys()))

    @Slot(str)
    def on_error_occurred(self, error_msg: str):
        logger.error(f"Worker report error: {error_msg}")

    @Slot()
    def on_config_changed(self):
        self.apply_theme()
        if self.worker:
            self.worker.update_interval(self.config.monitoring_interval)
            self.worker.update_selected_interface(self.config.selected_interface)
        
        self.dashboard_view.chart.set_max_samples(self.config.graph_time_window)

    def closeEvent(self, event):
        self.stop_monitoring()
        event.accept()
