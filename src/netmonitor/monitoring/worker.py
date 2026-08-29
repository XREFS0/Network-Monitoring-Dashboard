from PySide6.QtCore import QObject, Signal, Slot, QMutex, QMutexLocker
import time
from typing import Dict, List, Optional
from ..core.models import NetworkOverview, InterfaceStats, ConnectionInfo, SystemStats
from .samplers import NetworkSampler
from ..core.logger import setup_logger

logger = setup_logger()

class MonitoringWorker(QObject):
    data_sampled = Signal(NetworkOverview, dict, list, SystemStats)
    error_occurred = Signal(str)

    def __init__(self, interval: float, selected_interface: str):
        super().__init__()
        self.sampler = NetworkSampler()
        self.interval = interval
        self.selected_interface = selected_interface
        self.is_running = True
        self.mutex = QMutex()

    @Slot()
    def run(self):
        try:
            self.sampler.sample_interfaces()
            time.sleep(0.1)
        except Exception as e:
            logger.error(f"Initial sample failure: {e}")

        while True:
            with QMutexLocker(self.mutex):
                if not self.is_running:
                    break

            current_interval = self.interval
            current_selected = self.selected_interface

            try:
                interfaces = self.sampler.sample_interfaces()
                overview = self.sampler.get_network_overview(interfaces, current_selected)
                connections = self.sampler.sample_connections()
                sys_stats = self.sampler.get_system_stats()

                self.data_sampled.emit(overview, interfaces, connections, sys_stats)
            except Exception as e:
                logger.error(f"Sampling failure: {e}")
                self.error_occurred.emit(str(e))

            time.sleep(current_interval)

    @Slot()
    def stop(self):
        with QMutexLocker(self.mutex):
            self.is_running = False

    @Slot(float)
    def update_interval(self, interval: float):
        with QMutexLocker(self.mutex):
            self.interval = interval

    @Slot(str)
    def update_selected_interface(self, interface: str):
        with QMutexLocker(self.mutex):
            self.selected_interface = interface
