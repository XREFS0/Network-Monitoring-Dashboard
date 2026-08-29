import sys
from PySide6.QtWidgets import QApplication
from .core.logger import setup_logger
from .ui.mainwindow import MainWindow

def main():
    logger = setup_logger()
    logger.info("Initializing Network Monitoring Dashboard")

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
