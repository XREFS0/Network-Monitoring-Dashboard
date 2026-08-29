from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QLabel, QFrame, QGridLayout, QListWidgetItem
from PySide6.QtCore import Qt
from ...utils.formatting import format_bytes, format_speed
from ...core.models import InterfaceStats

class InterfacesView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)

        self.left_panel = QVBoxLayout()
        self.left_panel.setSpacing(10)
        
        self.list_label = QLabel("ADAPTERS")
        self.list_label.setObjectName("CardTitle")
        self.left_panel.addWidget(self.list_label)

        self.list_widget = QListWidget()
        self.list_widget.setFixedWidth(200)
        self.list_widget.currentRowChanged.connect(self.on_selection_changed)
        self.left_panel.addWidget(self.list_widget)

        self.layout.addLayout(self.left_panel)

        self.right_panel = QFrame()
        self.right_panel.setObjectName("Card")
        self.right_layout = QVBoxLayout(self.right_panel)
        self.right_layout.setContentsMargins(20, 20, 20, 20)
        self.right_layout.setSpacing(15)

        self.title_label = QLabel("Select an interface")
        self.title_label.setObjectName("CardTitle")
        self.right_layout.addWidget(self.title_label)

        self.grid = QGridLayout()
        self.grid.setSpacing(12)

        self.labels = {}
        fields = [
            ("Status", "Operational Status"),
            ("IPv4", "IPv4 Address"),
            ("IPv6", "IPv6 Address"),
            ("MAC", "MAC Address"),
            ("LinkSpeed", "Link Speed"),
            ("MTU", "MTU"),
            ("TxSpeed", "Upload Speed"),
            ("RxSpeed", "Download Speed"),
            ("Sent", "Total Sent"),
            ("Recv", "Total Received"),
            ("PktsSent", "Packets Sent"),
            ("PktsRecv", "Packets Received"),
            ("ErrIn", "Receive Errors"),
            ("ErrOut", "Transmit Errors"),
            ("DropIn", "Receive Drops"),
            ("DropOut", "Transmit Drops")
        ]

        for idx, (key, label_text) in enumerate(fields):
            row = idx % 8
            col = (idx // 8) * 2
            
            lbl_title = QLabel(label_text + ":")
            lbl_title.setStyleSheet("font-weight: 600; color: #94a3b8;")
            lbl_val = QLabel("--")
            
            self.grid.addWidget(lbl_title, row, col)
            self.grid.addWidget(lbl_val, row, col + 1)
            self.labels[key] = lbl_val

        self.right_layout.addLayout(self.grid)
        self.right_layout.addStretch()

        self.layout.addWidget(self.right_panel, 1)

        self.interfaces_data = {}
        self.selected_interface = None

    def update_data(self, interfaces: dict[str, InterfaceStats]):
        self.interfaces_data = interfaces
        
        current_selection = self.selected_interface
        
        self.list_widget.blockSignals(True)
        self.list_widget.clear()
        
        for idx, name in enumerate(sorted(interfaces.keys())):
            status = "UP" if interfaces[name].is_up else "DOWN"
            item = QListWidgetItem(f"{name} ({status})")
            item.setData(Qt.UserRole, name)
            self.list_widget.addItem(item)
            
            if name == current_selection:
                self.list_widget.setCurrentRow(idx)
                
        self.list_widget.blockSignals(False)

        if not self.selected_interface and interfaces:
            self.list_widget.setCurrentRow(0)
        else:
            self.refresh_details()

    def on_selection_changed(self, row: int):
        item = self.list_widget.item(row)
        if item:
            self.selected_interface = item.data(Qt.UserRole)
            self.refresh_details()

    def refresh_details(self):
        if not self.selected_interface or self.selected_interface not in self.interfaces_data:
            self.title_label.setText("No interface selected")
            for lbl in self.labels.values():
                lbl.setText("--")
            return

        info = self.interfaces_data[self.selected_interface]
        self.title_label.setText(info.name.upper())

        self.labels["Status"].setText("UP" if info.is_up else "DOWN")
        self.labels["IPv4"].setText(info.ipv4_address if info.ipv4_address else "N/A")
        self.labels["IPv6"].setText(info.ipv6_address if info.ipv6_address else "N/A")
        self.labels["MAC"].setText(info.mac_address if info.mac_address else "N/A")
        self.labels["LinkSpeed"].setText(f"{info.speed} Mbps" if info.speed > 0 else "Unknown")
        self.labels["MTU"].setText(str(info.mtu))
        self.labels["TxSpeed"].setText(format_speed(info.bytes_sent_speed))
        self.labels["RxSpeed"].setText(format_speed(info.bytes_recv_speed))
        self.labels["Sent"].setText(format_bytes(info.bytes_sent))
        self.labels["Recv"].setText(format_bytes(info.bytes_recv))
        self.labels["PktsSent"].setText(str(info.packets_sent))
        self.labels["PktsRecv"].setText(str(info.packets_recv))
        self.labels["ErrIn"].setText(str(info.errin))
        self.labels["ErrOut"].setText(str(info.errout))
        self.labels["DropIn"].setText(str(info.dropin))
        self.labels["DropOut"].setText(str(info.dropout))
