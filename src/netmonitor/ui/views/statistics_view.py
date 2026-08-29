from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QHeaderView
from PySide6.QtCore import Qt
from ...utils.formatting import format_bytes
from ...core.models import InterfaceStats

class StatisticsView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        self.title_label = QLabel("DETAILED INTERFACE STATISTICS")
        self.title_label.setObjectName("CardTitle")
        self.layout.addWidget(self.title_label)

        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "Interface", "Bytes Sent", "Bytes Received",
            "Packets Sent", "Packets Received",
            "Errors In", "Errors Out", "Drops In", "Drops Out"
        ])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        
        self.table.setSortingEnabled(True)
        self.layout.addWidget(self.table)

    def update_data(self, interfaces: dict[str, InterfaceStats]):
        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(interfaces))
        
        for row, (name, info) in enumerate(sorted(interfaces.items())):
            items = [
                QTableWidgetItem(name),
                QTableWidgetItem(format_bytes(info.bytes_sent)),
                QTableWidgetItem(format_bytes(info.bytes_recv)),
                QTableWidgetItem(str(info.packets_sent)),
                QTableWidgetItem(str(info.packets_recv)),
                QTableWidgetItem(str(info.errin)),
                QTableWidgetItem(str(info.errout)),
                QTableWidgetItem(str(info.dropin)),
                QTableWidgetItem(str(info.dropout))
            ]
            
            for col, item in enumerate(items):
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                if col in [3, 4, 5, 6, 7, 8]:
                    item.setData(Qt.DisplayRole, int(item.text()))
                elif col in [1, 2]:
                    raw_val = info.bytes_sent if col == 1 else info.bytes_recv
                    item.setData(Qt.DisplayRole, raw_val)
                    item.setText(format_bytes(raw_val))
                
                self.table.setItem(row, col, item)

        self.table.setSortingEnabled(True)
