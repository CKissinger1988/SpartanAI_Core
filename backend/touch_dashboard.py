import sys
import math
import random
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, 
                               QLabel, QTextEdit, QHBoxLayout, QGridLayout, QLineEdit, 
                               QGraphicsDropShadowEffect, QSizePolicy)
from PySide6.QtCore import Qt, QSize, QTimer, QRect
from PySide6.QtGui import QColor, QBrush, QPen, QFont, QPainterPath

class WaveformViz(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(200, 50)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)
        self.offset = 0
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(QColor(0, 255, 204), 2))
        path = QPainterPath()
        path.moveTo(0, 25)
        for x in range(200):
            y = 25 + 15 * math.sin((x + self.offset) * 0.1)
            path.lineTo(x, y)
        painter.drawPath(path)
        self.offset += 1

class TouchDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SpartanAI - Apex Touch")
        self.setStyleSheet("background-color: #050505; color: #00ffcc;")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        
        # Central widget for touch layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        # Title
        title = QLabel("APEX TACTICAL")
        title.setFont(QFont("Courier New", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(title)
        
        # Neural Waveform
        self.viz = WaveformViz()
        self.layout.addWidget(self.viz, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Command Status
        self.status_label = QLabel("STATUS: IDLE")
        self.status_label.setStyleSheet("color: #00ffcc; font-size: 16px; font-weight: bold;")
        self.layout.addWidget(self.status_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Tactical Grid (Touch friendly)
        grid = QGridLayout()
        grid.setSpacing(15)
        btn_style = "QPushButton { background-color: #1a1a1a; color: #00ffcc; border: 2px solid #00ffcc; border-radius: 15px; font-size: 18px; padding: 25px; } QPushButton:pressed { background-color: #00ffcc; color: #000; }"
        
        btns = [("SYS STATUS", "systems status"), ("NET RECON", "analyze network"), 
                ("DEPLOY", "deploy_mesh"), ("ISO SECURE", "encrypt_iso"), 
                ("S.T.E.P.P.", "stepp_audit"), ("SYNC", "sync_brain")]
        
        for i, (text, cmd) in enumerate(btns):
            btn = QPushButton(text)
            btn.setStyleSheet(btn_style)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            btn.clicked.connect(lambda checked, c=cmd: self.quick_command(c))
            grid.addWidget(btn, i // 2, i % 2)
        
        self.layout.addLayout(grid)
        
        # Chat area
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setStyleSheet("background-color: #000; color: #fff; font-size: 16px; border: 1px solid #333;")
        self.layout.addWidget(self.chat_area)
        
        self.showMaximized()

    def quick_command(self, cmd):
        self.status_label.setText(f"STATUS: RUNNING {cmd}")
        self.chat_area.append(f">> Executing: {cmd}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    touch_dash = TouchDashboard()
    touch_dash.show()
    sys.exit(app.exec())
