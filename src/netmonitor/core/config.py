import os
import json
from pathlib import Path

class AppConfig:
    def __init__(self):
        self.config_dir = Path(os.path.expanduser("~")) / ".netmonitor"
        self.config_file = self.config_dir / "config.json"
        self.monitoring_interval = 1.0
        self.graph_time_window = 60
        self.selected_interface = ""
        self.theme = "dark"
        self.start_automatically = True
        self.load()

    def load(self):
        if not self.config_file.exists():
            return
        try:
            with open(self.config_file, "r") as f:
                data = json.load(f)
                self.monitoring_interval = float(data.get("monitoring_interval", 1.0))
                self.graph_time_window = int(data.get("graph_time_window", 60))
                self.selected_interface = data.get("selected_interface", "")
                self.theme = data.get("theme", "dark")
                self.start_automatically = bool(data.get("start_automatically", True))
        except Exception:
            pass

    def save(self):
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            data = {
                "monitoring_interval": self.monitoring_interval,
                "graph_time_window": self.graph_time_window,
                "selected_interface": self.selected_interface,
                "theme": self.theme,
                "start_automatically": self.start_automatically
            }
            with open(self.config_file, "w") as f:
                json.dump(data, f, indent=4)
        except Exception:
            pass
