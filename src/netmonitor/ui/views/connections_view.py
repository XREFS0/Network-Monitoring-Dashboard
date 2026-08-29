from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QLineEdit, QLabel, QHeaderView
from PySide6.QtCore import Qt
from ...core.models import ConnectionInfo

class ConnectionsView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        self.top_bar = QHBoxLayout()
        self.title_label = QLabel("ACTIVE CONNECTIONS")
        self.title_label.setObjectName("CardTitle")
        self.top_bar.addWidget(self.title_label)

        self.top_bar.addStretch()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by process, address, port, status...")
        self.search_input.setFixedWidth(300)
        self.search_input.textChanged.connect(self.filter_connections)
        self.top_bar.addWidget(self.search_input)

        self.layout.addLayout(self.top_bar)

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Protocol", "Local Address", "Local Port",
            "Remote Address", "Remote Port", "Status",
            "PID", "Process Name"
        ])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        
        self.table.setSortingEnabled(True)
        self.layout.addWidget(self.table)

        self.connections_data = []

    def update_data(self, connections: list[ConnectionInfo]):
        self.connections_data = connections
        self.populate_table()

    def populate_table(self):
        self.table.setSortingEnabled(False)
        
        filter_text = self.search_input.text().lower()
        
        filtered = []
        for c in self.connections_data:
            match = (
                not filter_text or
                filter_text in c.protocol.lower() or
                filter_text in c.local_address.lower() or
                filter_text in str(c.local_port) or
                filter_text in c.remote_address.lower() or
                filter_text in str(c.remote_port) or
                filter_text in c.status.lower() or
                (c.pid and filter_text in str(c.pid)) or
                (c.process_name and filter_text in c.process_name.lower())
            )
            if match:
                filtered.append(c)

        self.table.setRowCount(len(filtered))
        for row, c in enumerate(filtered):
            items = [
                QTableWidgetItem(c.protocol),
                QTableWidgetItem(c.local_address),
                QTableWidgetItem(str(c.local_port)),
                QTableWidgetItem(c.remote_address),
                QTableWidgetItem(str(c.remote_port)),
                QTableWidgetItem(c.status),
                QTableWidgetItem(str(c.pid) if c.pid is not None else ""),
                QTableWidgetItem(c.process_name if c.process_name else "")
            ]
            
            for col, item in enumerate(items):
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                
                if col in [2, 4, 6]:
                    val = int(item.text()) if item.text() else -1
                    item.setData(Qt.DisplayRole, val if val != -1 else "")
                
                self.table.setItem(row, col, item)

        self.table.setSortingEnabled(True)

    def filter_connections(self):
        self.populate_table()
