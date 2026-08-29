from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QComboBox, QCheckBox, QPushButton, QFrame
from PySide6.QtCore import Signal
from ...core.config import AppConfig

class SettingsView(QWidget):
    config_changed = Signal()

    def __init__(self, config: AppConfig, parent=None):
        super().__init__(parent)
        self.config = config
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)

        self.title_label = QLabel("SETTINGS")
        self.title_label.setObjectName("CardTitle")
        self.layout.addWidget(self.title_label)

        self.form_frame = QFrame()
        self.form_frame.setObjectName("Card")
        self.form_layout = QGridLayout(self.form_frame)
        self.form_layout.setContentsMargins(20, 20, 20, 20)
        self.form_layout.setSpacing(15)

        self.form_layout.addWidget(QLabel("Theme:"), 0, 0)
        self.combo_theme = QComboBox()
        self.combo_theme.addItems(["Dark", "Light"])
        self.combo_theme.setCurrentText("Dark" if self.config.theme == "dark" else "Light")
        self.form_layout.addWidget(self.combo_theme, 0, 1)

        self.form_layout.addWidget(QLabel("Monitoring Interval:"), 1, 0)
        self.combo_interval = QComboBox()
        self.combo_interval.addItems(["0.5 seconds", "1.0 seconds", "2.0 seconds", "5.0 seconds", "10.0 seconds"])
        interval_map = {0.5: "0.5 seconds", 1.0: "1.0 seconds", 2.0: "2.0 seconds", 5.0: "5.0 seconds", 10.0: "10.0 seconds"}
        self.combo_interval.setCurrentText(interval_map.get(self.config.monitoring_interval, "1.0 seconds"))
        self.form_layout.addWidget(self.combo_interval, 1, 1)

        self.form_layout.addWidget(QLabel("Graph Time Window:"), 2, 0)
        self.combo_window = QComboBox()
        self.combo_window.addItems(["30 seconds", "60 seconds", "120 seconds", "300 seconds"])
        window_map = {30: "30 seconds", 60: "60 seconds", 120: "120 seconds", 300: "300 seconds"}
        self.combo_window.setCurrentText(window_map.get(self.config.graph_time_window, "60 seconds"))
        self.form_layout.addWidget(self.combo_window, 2, 1)

        self.form_layout.addWidget(QLabel("Default Monitored Interface:"), 3, 0)
        self.combo_interface = QComboBox()
        self.combo_interface.addItem("Auto-detect Active", "")
        self.form_layout.addWidget(self.combo_interface, 3, 1)

        self.chk_auto = QCheckBox("Start monitoring automatically on startup")
        self.chk_auto.setChecked(self.config.start_automatically)
        self.form_layout.addWidget(self.chk_auto, 4, 0, 1, 2)

        self.layout.addWidget(self.form_frame)

        self.btn_save = QPushButton("Save Settings")
        self.btn_save.setFixedWidth(120)
        self.btn_save.clicked.connect(self.save_settings)
        self.layout.addWidget(self.btn_save)

        self.layout.addStretch()

    def update_interfaces(self, interface_names: list[str]):
        current_data = self.combo_interface.currentData()
        
        self.combo_interface.blockSignals(True)
        self.combo_interface.clear()
        self.combo_interface.addItem("Auto-detect Active", "")
        
        for name in sorted(interface_names):
            self.combo_interface.addItem(name, name)
            
        index = self.combo_interface.findData(current_data)
        if index != -1:
            self.combo_interface.setCurrentIndex(index)
        else:
            saved_index = self.combo_interface.findData(self.config.selected_interface)
            if saved_index != -1:
                self.combo_interface.setCurrentIndex(saved_index)
                
        self.combo_interface.blockSignals(False)

    def save_settings(self):
        self.config.theme = self.combo_theme.currentText().lower()
        
        interval_val = float(self.combo_interval.currentText().split()[0])
        self.config.monitoring_interval = interval_val
        
        window_val = int(self.combo_window.currentText().split()[0])
        self.config.graph_time_window = window_val
        
        self.config.selected_interface = self.combo_interface.currentData()
        self.config.start_automatically = self.chk_auto.isChecked()
        
        self.config.save()
        self.config_changed.emit()
