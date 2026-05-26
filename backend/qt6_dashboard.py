import sys
import os
import random
import math
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, 
                             QPushButton, QLabel, QTextEdit, QHBoxLayout, 
                             QLineEdit, QSystemTrayIcon, QMenu)
from PySide6.QtCore import Qt, QPoint, QSize, QTimer
from PySide6.QtGui import QMouseEvent, QFont, QIcon, QAction, QColor

class GhostWidget(QMainWindow):
    """
    SpartanAI Ghost Widget (RESTORED AESTHETICS).
    Original Streamlabs-style high-transparency chatbox with Sovereign enhancements.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SpartanAI - Ghost")
        
        # Transparent, Frameless, Tool Window (Always on Top)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        
        self.expanded = False
        self.oldPos = self.pos()
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Original Toggle Button (Circular)
        self.toggle_btn = QPushButton("??")
        self.toggle_btn.setFixedSize(50, 50)
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(20, 20, 20, 180); 
                color: #00ffcc; 
                border-radius: 25px; 
                font-size: 24px;
                border: 1px solid #00ffcc;
            }
            QPushButton:hover {
                background-color: rgba(0, 255, 204, 50);
            }
        """)
        self.toggle_btn.clicked.connect(self.toggle_dashboard)
        self.layout.addWidget(self.toggle_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Dashboard Container (Restored Streamlabs Look)
        self.dashboard_container = QWidget()
        self.dash_layout = QVBoxLayout(self.dashboard_container)
        self.dash_layout.setContentsMargins(5, 5, 5, 5)
        
        # Streamlabs-style Chatbox Aesthetics
        chat_style = """
            QTextEdit {
                background-color: rgba(0, 0, 0, 120); 
                color: #ffffff; 
                border: none; 
                border-radius: 5px; 
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                padding: 5px;
            }
        """
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setStyleSheet(chat_style)
        self.chat_area.setText(">> Jarvis // Core Initialized.")
        self.dash_layout.addWidget(self.chat_area)
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Command...")
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: rgba(20, 20, 20, 200); 
                color: #00ffcc; 
                border: none; 
                border-bottom: 2px solid #00ffcc; 
                font-family: 'Segoe UI'; 
                font-size: 12px; 
                padding: 5px;
            }
        """)
        self.input_field.returnPressed.connect(self.send_command)
        self.dash_layout.addWidget(self.input_field)
        
        self.dashboard_container.setStyleSheet("background-color: rgba(0, 0, 0, 150); border: 1px solid #333; border-radius: 10px;")
        self.dashboard_container.setVisible(False)
        self.layout.addWidget(self.dashboard_container)
        
        self.resize(60, 60)
        self.snap_to_bottom_right()

    def send_command(self):
        text = self.input_field.text()
        if text:
            # Styled chat output
            self.chat_area.append(f'<span style="color: #00ffcc; font-weight: bold;">[OPERATOR]:</span> <span style="color: white;">{text}</span>')
            self.input_field.clear()
            # Simulation of Jarvis response
            QTimer.singleShot(600, lambda: self.chat_area.append(
                f'<span style="color: #00ff44; font-weight: bold;">[JARVIS]:</span> Execution path verified. Task complete.'
            ))

    def snap_to_bottom_right(self):
        screen_geom = QApplication.primaryScreen().availableGeometry()
        x = screen_geom.width() - self.width() - 20
        y = screen_geom.height() - self.height() - 20
        self.move(x, y)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.LeftButton:
            delta = QPoint(event.globalPosition().toPoint() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPosition().toPoint()

    def toggle_dashboard(self):
        self.expanded = not self.expanded
        self.dashboard_container.setVisible(self.expanded)
        if self.expanded:
            self.resize(350, 400)
            self.toggle_btn.setText("??")
        else:
            self.resize(60, 60)
            self.toggle_btn.setText("??")
        self.snap_to_bottom_right()

class SpartanTrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Using a default system icon if none found
        self.setIcon(QIcon.fromTheme("security-high", QIcon()))
        
        self.menu = QMenu()
        self.show_action = QAction("Open Command Hub")
        self.show_action.triggered.connect(self.parent().showNormal)
        self.menu.addAction(self.show_action)
        
        self.ghost_action = QAction("Toggle Ghost Chat")
        self.ghost_action.triggered.connect(self.parent().toggle_dashboard)
        self.menu.addAction(self.ghost_action)
        
        self.menu.addSeparator()
        self.exit_action = QAction("Sovereign Shutdown")
        self.exit_action.triggered.connect(QApplication.instance().quit)
        self.menu.addAction(self.exit_action)
        
        self.setContextMenu(self.menu)
        self.setToolTip("SpartanAI Sovereign Core")

if __name__ == "__main__":
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    ghost = GhostWidget()
    tray = SpartanTrayIcon(ghost)
    tray.show()
    
    ghost.show()
    print("[DESKTOP]: Ghost Widget (Restored Aesthetics) Online.")
    sys.exit(app.exec())
