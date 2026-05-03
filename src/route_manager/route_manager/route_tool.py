import sys
import os
import yaml
import math
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton,
    QFileDialog, QVBoxLayout, QWidget, QListWidget, QMessageBox
)
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt, QPoint, QTimer

class MapWidget(QLabel):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)

        self.points = []
        self.current_start = None

        self.map_yaml = None
        self.map_resolution = 1.0
        self.map_origin = [0, 0]

    def load_map(self, yaml_path):
        with open(yaml_path, 'r') as f:
            self.map_yaml = yaml.safe_load(f)

        img_path = self.map_yaml['image']
        if not os.path.isabs(img_path):
            img_path = os.path.join(os.path.dirname(yaml_path), img_path)

        self.map_resolution = self.map_yaml['resolution']
        self.map_origin = self.map_yaml['origin']

        pixmap = QPixmap(img_path)
        if pixmap.isNull():
            raise ValueError(f"Cannot load map image: {img_path}")

        self.setPixmap(pixmap)
        self.adjustSize()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.current_start = event.pos()

    def mouseReleaseEvent(self, event):
        if self.current_start is None:
            return

        end = event.pos()

        # pixel → map
        x1, y1 = self.pixel_to_map(self.current_start)
        x2, y2 = self.pixel_to_map(end)

        yaw = math.atan2(y2 - y1, x2 - x1)

        self.points.append({
            "x": x1,
            "y": y1,
            "yaw": yaw
        })

        self.current_start = None
        self.update()

    def pixel_to_map(self, p):
        px = p.x()
        py = p.y()

        height = self.pixmap().height()

        mx = px * self.map_resolution + self.map_origin[0]
        my = (height - py) * self.map_resolution + self.map_origin[1]

        return mx, my

    def paintEvent(self, event):
        super().paintEvent(event)

        if not self.points:
            return

        painter = QPainter(self)
        pen = QPen(Qt.red, 3)
        painter.setPen(pen)

        for p in self.points:
            px, py = self.map_to_pixel(p["x"], p["y"])
            painter.drawEllipse(QPoint(px, py), 5, 5)

            # vẽ hướng
            dx = 20 * math.cos(p["yaw"])
            dy = -20 * math.sin(p["yaw"])
            painter.drawLine(px, py, px + dx, py + dy)

    def map_to_pixel(self, x, y):
        height = self.pixmap().height()

        px = int((x - self.map_origin[0]) / self.map_resolution)
        py = int(height - (y - self.map_origin[1]) / self.map_resolution)

        return px, py


class RouteGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AGV Route Tool")

        self.map_widget = MapWidget()
        self.list_widget = QListWidget()

        load_btn = QPushButton("Load Map")
        save_btn = QPushButton("Save Route")
        clear_btn = QPushButton("Clear")

        load_btn.clicked.connect(self.load_map)
        save_btn.clicked.connect(self.save_route)
        clear_btn.clicked.connect(self.clear_points)

        layout = QVBoxLayout()
        layout.addWidget(load_btn)
        layout.addWidget(save_btn)
        layout.addWidget(clear_btn)
        layout.addWidget(self.map_widget)
        layout.addWidget(self.list_widget)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        self.timer_update_list()

    def load_map(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select map yaml")
        if path:
            try:
                self.map_widget.load_map(path)
                self.map_widget.points = []
                self.list_widget.clear()
            except Exception as exc:
                QMessageBox.critical(self, "Load map failed", str(exc))

    def save_route(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save route", "route.yaml")
        if not path:
            return

        data = {"route": []}

        for i, p in enumerate(self.map_widget.points):
            data["route"].append({
                "name": f"P{i+1}",
                "x": p["x"],
                "y": p["y"],
                "yaw": p["yaw"]
            })

        with open(path, "w") as f:
            yaml.dump(data, f)

    def clear_points(self):
        self.map_widget.points = []
        self.map_widget.update()

    def timer_update_list(self):
        self.list_widget.clear()
        for i, p in enumerate(self.map_widget.points):
            self.list_widget.addItem(f"P{i+1}: x={p['x']:.2f}, y={p['y']:.2f}")

        QTimer.singleShot(500, self.timer_update_list)


def main():
    app = QApplication(sys.argv)
    window = RouteGUI()
    window.show()
    sys.exit(app.exec_())
