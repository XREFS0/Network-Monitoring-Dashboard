from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QPainterPath, QBrush
from PySide6.QtCore import Qt, QPointF
from collections import deque
from ...utils.formatting import format_speed

class TrafficChart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.max_samples = 60
        self.download_history = deque(maxlen=self.max_samples)
        self.upload_history = deque(maxlen=self.max_samples)
        self.is_dark = True

        for _ in range(self.max_samples):
            self.download_history.append(0.0)
            self.upload_history.append(0.0)

    def set_theme(self, is_dark: bool):
        self.is_dark = is_dark
        self.update()

    def set_max_samples(self, count: int):
        self.max_samples = count
        new_dl = deque(self.download_history, maxlen=count)
        new_ul = deque(self.upload_history, maxlen=count)
        while len(new_dl) < count:
            new_dl.appendleft(0.0)
        while len(new_ul) < count:
            new_ul.appendleft(0.0)
        self.download_history = new_dl
        self.upload_history = new_ul
        self.update()

    def add_sample(self, download_speed: float, upload_speed: float):
        self.download_history.append(download_speed)
        self.upload_history.append(upload_speed)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()

        bg_color = QColor("#242936") if self.is_dark else QColor("#ffffff")
        border_color = QColor("#2d3139") if self.is_dark else QColor("#e2e8f0")
        grid_color = QColor("#2d3139") if self.is_dark else QColor("#f1f5f9")
        text_color = QColor("#94a3b8") if self.is_dark else QColor("#64748b")
        dl_color = QColor("#3b82f6")
        ul_color = QColor("#f59e0b")

        painter.fillRect(0, 0, w, h, bg_color)
        painter.setPen(QPen(border_color, 1))
        painter.drawRect(0, 0, w - 1, h - 1)

        padding_left = 70
        padding_right = 20
        padding_top = 20
        padding_bottom = 20

        chart_w = w - padding_left - padding_right
        chart_h = h - padding_top - padding_bottom

        if chart_w <= 0 or chart_h <= 0:
            painter.end()
            return

        max_val = max(max(self.download_history), max(self.upload_history))
        if max_val < 1024.0:
            max_val = 1024.0

        painter.setFont(QFont("Segoe UI", 9))
        painter.setPen(QPen(text_color, 1))
        grid_steps = 4
        for i in range(grid_steps + 1):
            val = (max_val / grid_steps) * i
            y = padding_top + chart_h - int((chart_h / grid_steps) * i)
            painter.drawText(10, y + 4, format_speed(val))
            painter.setPen(QPen(grid_color, 1, Qt.DashLine))
            painter.drawLine(padding_left, y, padding_left + chart_w, y)
            painter.setPen(QPen(text_color, 1))

        time_steps = 5
        for i in range(time_steps):
            x = padding_left + int((chart_w / (time_steps - 1)) * i)
            seconds_ago = int((self.max_samples / (time_steps - 1)) * (time_steps - 1 - i))
            painter.drawText(x - 10, h - 4, f"-{seconds_ago}s")
            painter.setPen(QPen(grid_color, 1, Qt.DashLine))
            painter.drawLine(x, padding_top, x, padding_top + chart_h)
            painter.setPen(QPen(text_color, 1))

        def draw_line(history, color):
            path = QPainterPath()
            points = []
            for idx, speed in enumerate(history):
                x = padding_left + (chart_w / (self.max_samples - 1)) * idx
                y = padding_top + chart_h - (chart_h * (speed / max_val))
                points.append(QPointF(x, y))

            if points:
                path.moveTo(points[0])
                for pt in points[1:]:
                    path.lineTo(pt)
                painter.setPen(QPen(color, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                painter.drawPath(path)

                fill_path = QPainterPath(path)
                fill_path.lineTo(points[-1].x(), padding_top + chart_h)
                fill_path.lineTo(points[0].x(), padding_top + chart_h)
                fill_path.closeSubpath()
                fill_color = QColor(color.red(), color.green(), color.blue(), 25)
                painter.fillPath(fill_path, QBrush(fill_color))

        draw_line(self.download_history, dl_color)
        draw_line(self.upload_history, ul_color)

        painter.setPen(QPen(dl_color, 4))
        painter.drawPoint(padding_left + 10, padding_top - 10)
        painter.setPen(QPen(text_color, 1))
        painter.drawText(padding_left + 18, padding_top - 6, "Download")

        painter.setPen(QPen(ul_color, 4))
        painter.drawPoint(padding_left + 100, padding_top - 10)
        painter.setPen(QPen(text_color, 1))
        painter.drawText(padding_left + 108, padding_top - 6, "Upload")

        painter.end()
