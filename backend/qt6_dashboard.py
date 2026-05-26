import sys
import os
import random
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, 
                             QPushButton, QLabel, QTextEdit, QHBoxLayout, 
                             QLineEdit, QSystemTrayIcon, QMenu)
from PySide6.QtCore import Qt, QPoint, QSize, QTimer
from PySide6.QtGui import QMouseEvent, QFont, QIcon, QAction, QColor

# Note: In production, this would import the Jarvis core
# from backend.core.CognitiveCore.jarvis import Jarvis

class GhostChatWidget(QMainWindow):
    """
    SentinelAI Ghost Chat Widget (v50-SUPREME).
    A high-entropy, transparent, draggable overlay for direct interaction with Jarvis.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SentinelAI - Ghost")
        
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
        
        # Ghost Toggle (The Sentinel Eye)
        self.toggle_btn = QPushButton("??")
        self.toggle_btn.setFixedSize(60, 60)
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 255, 204, 30); 
                color: #00ffcc; 
                border: 2px solid #00ffcc;
                border-radius: 30px; 
                font-size: 28px;
            }
            QPushButton:hover {
                background-color: rgba(0, 255, 204, 80);
                box-shadow: 0 0 20px #00ffcc;
            }
        """)
        self.toggle_btn.clicked.connect(self.toggle_dashboard)
        self.layout.addWidget(self.toggle_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Dashboard Container
        self.dashboard_container = QWidget()
        self.dash_layout = QVBoxLayout(self.dashboard_container)
        self.dash_layout.setContentsMargins(10, 10, 10, 10)
        
        # Stylized Chat Area
        chat_style = """
            QTextEdit {
                background-color: rgba(5, 5, 5, 200); 
                color: #ffffff; 
                border: 1px solid #00ffcc; 
                border-radius: 5px; 
                font-family: 'Consolas', monospace;
                font-size: 13px;
            }
        """
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setStyleSheet(chat_style)
        self.chat_area.append('<span style="color: #00ffcc;">>> Jarvis // Omni-Cognitive Assembly ACTIVE.</span>')
        self.dash_layout.addWidget(self.chat_area)
        
        # Input Field
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Direct Directive...")
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: rgba(20, 20, 20, 230); 
                color: #00ffcc; 
                border: none; 
                border-bottom: 2px solid #00ffcc; 
                font-family: 'Consolas'; 
                font-size: 14px; 
                padding: 8px;
            }
        """)
        self.input_field.returnPressed.connect(self.send_directive)
        self.dash_layout.addWidget(self.input_field)
        
        self.dashboard_container.setStyleSheet("background-color: rgba(10, 10, 12, 180); border-radius: 12px;")
        self.dashboard_container.setVisible(False)
        self.layout.addWidget(self.dashboard_container)
        
        self.resize(70, 70)
        self.snap_to_bottom_right()

    def send_directive(self):
        directive = self.input_field.text()
        if directive:
            self.chat_area.append(f'<span style="color: #00ffcc; font-weight: bold;">[CREATOR]:</span> {directive}')
            self.input_field.clear()
            
            # Autonomous Response (Simulating Jarvis Assembly)
            QTimer.singleShot(500, lambda: self.chat_area.append(
                f'<span style="color: #00ff44;">[JARVIS]:</span> Executing sovereign task. Result: SUCCESS.'
            ))

    def snap_to_bottom_right(self):
        screen_geom = QApplication.primaryScreen().availableGeometry()
        x = screen_geom.width() - self.width() - 30
        y = screen_geom.height() - self.height() - 30
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
            self.resize(400, 500)
            self.toggle_btn.setText("??")
        else:
            self.resize(70, 70)
            self.toggle_btn.setText("??")
        self.snap_to_bottom_right()

class SentinelTrayIcon(QSystemTrayIcon):
    """
    Sovereign Taskbar Icon.
    Provides persistent access to the Command Hub.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setIcon(QIcon.fromTheme("security-high", QIcon())) # Fallback icon
        
        # Context Menu
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
        self.setToolTip("SentinelAI Sovereign Core")

if __name__ == "__main__":
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False) # Keep running in background
    
    ghost = GhostChatWidget()
    
    # Setup Tray Icon
    tray = SentinelTrayIcon(ghost)
    tray.show()
    
    ghost.show()
    
    print("[DESKTOP]: QT6 Sovereign Dashboard and Ghost Chat Online.")
    sys.exit(app.exec())
