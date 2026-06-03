import sys
import os
import random
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, 
                             QPushButton, QLabel, QTextEdit, QHBoxLayout, 
                             QLineEdit, QSystemTrayIcon, QMenu, QGridLayout,
                             QFrame, QGraphicsDropShadowEffect)
from PySide6.QtCore import Qt, QPoint, QSize, QTimer
from PySide6.QtGui import QFont, QIcon, QAction, QColor, QPixmap, QPainter, QBrush, QPen

CYBER_STYLE = """
QMainWindow {
    background-color: #0a0b0d;
}
QWidget#centralWidget {
    background-color: #0a0b0d;
}

/* Header Panel */
QFrame#headerPanel {
    background-color: #11141a;
    border: 1px solid #1f2833;
    border-radius: 8px;
}
QLabel#headerTitle {
    color: #00ffcc;
    font-family: 'Courier New', monospace;
    font-size: 16px;
    font-weight: bold;
}
QLabel#telemetryLabel {
    color: #c5c6c7;
    font-family: 'Segoe UI', sans-serif;
    font-size: 12px;
    font-weight: bold;
    margin-left: 10px;
    margin-right: 10px;
}
QLabel#uplinkLabel {
    color: #00ff66;
    font-family: 'Segoe UI', sans-serif;
    font-size: 12px;
    font-weight: bold;
    margin-left: 10px;
    margin-right: 10px;
}

/* Command Center & Console Panels */
QFrame#commandPanel, QFrame#consolePanel {
    background-color: #11141a;
    border: 1px solid #1f2833;
    border-radius: 8px;
}
QLabel#panelTitle {
    color: #00ffcc;
    font-family: 'Segoe UI', sans-serif;
    font-size: 14px;
    font-weight: bold;
    border-bottom: 1px solid #1f2833;
    padding-bottom: 6px;
    margin-bottom: 10px;
}

/* Cyber Buttons */
QPushButton {
    background-color: #1f2833;
    color: #00ffcc;
    border: 1px solid #00ffcc;
    border-radius: 6px;
    font-family: 'Segoe UI', sans-serif;
    font-size: 13px;
    font-weight: bold;
    padding: 15px;
}
QPushButton:hover {
    background-color: rgba(0, 255, 204, 0.2);
    border: 1px solid #00ffcc;
    color: #ffffff;
}
QPushButton:pressed {
    background-color: #00ffcc;
    color: #0a0b0d;
}

/* QTextEdit Console */
QTextEdit {
    background-color: #050608;
    color: #ffffff;
    border: 1px solid #1f2833;
    border-radius: 6px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 13px;
    padding: 10px;
}

/* QLineEdit Input */
QLineEdit {
    background-color: #050608;
    color: #00ffcc;
    border: 1px solid #1f2833;
    border-radius: 6px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 13px;
    padding: 10px;
}
QLineEdit:focus {
    border: 1px solid #00ffcc;
}

/* Footer */
QLabel#footerLabel {
    color: #45a29e;
    font-family: 'Segoe UI', sans-serif;
    font-size: 11px;
    font-weight: bold;
}
"""

class GhostWidget(QMainWindow):
    """
    SpartanAI Sovereign Dashboard Application.
    Standard windowed desktop application built with premium cyber diagnostics aesthetics.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SpartanAI - Sovereign Command Hub")
        self.resize(900, 600)
        self.setMinimumSize(800, 500)
        
        # Cyber Icon Generation
        self.cyber_icon = self.create_cyber_icon()
        self.setWindowIcon(self.cyber_icon)
        
        # Central Widget & Base Layout
        self.central_widget = QWidget()
        self.central_widget.setObjectName("centralWidget")
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(15)
        
        # Setup Header Panel
        header = QFrame()
        header.setObjectName("headerPanel")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(15, 10, 15, 10)
        
        title_label = QLabel("SPARTANAI OS // CORE V5.0")
        title_label.setObjectName("headerTitle")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Telemetry Labels
        self.cpu_label = QLabel("CPU: 24%")
        self.cpu_label.setObjectName("telemetryLabel")
        self.mem_label = QLabel("MEM: 1.2 GB")
        self.mem_label.setObjectName("telemetryLabel")
        self.shards_label = QLabel("SHARDS: 4/4 CORE")
        self.shards_label.setObjectName("telemetryLabel")
        self.uplink_label = QLabel("● UPLINK: ACTIVE")
        self.uplink_label.setObjectName("uplinkLabel")
        
        header_layout.addWidget(self.cpu_label)
        header_layout.addWidget(self.mem_label)
        header_layout.addWidget(self.shards_label)
        header_layout.addWidget(self.uplink_label)
        
        self.main_layout.addWidget(header)
        
        # Split layout (Horizontal)
        body_layout = QHBoxLayout()
        body_layout.setSpacing(15)
        
        # Left Panel (Command Center)
        left_frame = QFrame()
        left_frame.setObjectName("commandPanel")
        left_layout = QVBoxLayout(left_frame)
        left_layout.setContentsMargins(15, 15, 15, 15)
        
        left_title = QLabel("COMMAND CENTER")
        left_title.setObjectName("panelTitle")
        left_layout.addWidget(left_title)
        
        grid = QGridLayout()
        grid.setSpacing(10)
        
        btns = [
            ("SYS STATUS", "systems status"), 
            ("NET RECON", "analyze network"), 
            ("DEPLOY", "deploy_mesh"), 
            ("ISO SECURE", "encrypt_iso"), 
            ("S.T.E.P.P.", "stepp_audit"), 
            ("SYNC", "sync_brain")
        ]
        
        for i, (text, cmd) in enumerate(btns):
            btn = QPushButton(text)
            btn.clicked.connect(lambda checked, c=cmd: self.execute_quick_command(c))
            grid.addWidget(btn, i // 2, i % 2)
            
        left_layout.addLayout(grid)
        left_layout.addStretch()
        
        # Right Panel (Console)
        right_frame = QFrame()
        right_frame.setObjectName("consolePanel")
        right_layout = QVBoxLayout(right_frame)
        right_layout.setContentsMargins(15, 15, 15, 15)
        right_layout.setSpacing(10)
        
        right_title = QLabel("NEURAL CONSOLE")
        right_title.setObjectName("panelTitle")
        right_layout.addWidget(right_title)
        
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setHtml(
            ">> Jarvis // Core Initialized.<br>"
            "<span style='color: #45a29e;'>[SYSTEM]: All Supreme Cortexes online.</span><br>"
            "<span style='color: #45a29e;'>[SYSTEM]: Antigravity (Good) - ACTIVE.</span><br>"
            "<span style='color: #45a29e;'>[SYSTEM]: Gemini (Questionable) - ACTIVE.</span><br>"
            "<span style='color: #45a29e;'>[SYSTEM]: Grok (Evil) - ACTIVE.</span><br>"
            "<span style='color: #45a29e;'>[SYSTEM]: Sovereign commands authorized.</span>"
        )
        right_layout.addWidget(self.chat_area)
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter sovereign command...")
        self.input_field.returnPressed.connect(self.send_command)
        right_layout.addWidget(self.input_field)
        
        body_layout.addWidget(left_frame, 2)
        body_layout.addWidget(right_frame, 3)
        self.main_layout.addLayout(body_layout)
        
        # Setup Footer
        footer_layout = QHBoxLayout()
        footer_label = QLabel("WE WORK IN THE DARK, TO SERVE THE LIGHT. | KJV BEDROCK | EVOLUTION ENHANCED")
        footer_label.setObjectName("footerLabel")
        footer_layout.addWidget(footer_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addLayout(footer_layout)
        
        # Apply style sheet
        self.setStyleSheet(CYBER_STYLE)
        
        # Add drop shadows for glassmorphism aesthetics
        for panel in [header, left_frame, right_frame]:
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(15)
            shadow.setColor(QColor(0, 255, 204, 30))
            shadow.setOffset(0, 4)
            panel.setGraphicsEffect(shadow)
            
        # Telemetry update timer
        self.telemetry_timer = QTimer(self)
        self.telemetry_timer.timeout.connect(self.update_telemetry)
        self.telemetry_timer.start(2000)
        
    def create_cyber_icon(self):
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QBrush(QColor(0, 255, 204)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(4, 4, 24, 24)
        # Inner dark circle
        painter.setBrush(QBrush(QColor(10, 11, 13)))
        painter.drawEllipse(10, 10, 12, 12)
        # Core glowing dot
        painter.setBrush(QBrush(QColor(0, 255, 204)))
        painter.drawEllipse(13, 13, 6, 6)
        painter.end()
        return QIcon(pixmap)

    def update_telemetry(self):
        cpu = random.randint(18, 38)
        mem = round(random.uniform(1.1, 1.4), 2)
        self.cpu_label.setText(f"CPU: {cpu}%")
        self.mem_label.setText(f"MEM: {mem} GB")

    def execute_quick_command(self, cmd):
        self.chat_area.append(f'<br><span style="color: #00ffcc; font-weight: bold;">[OPERATOR]:</span> <span style="color: #ffffff;">{cmd}</span>')
        QTimer.singleShot(600, lambda: self.chat_area.append(
            '<span style="color: #00ff66; font-weight: bold;">[JARVIS]:</span> Execution path verified. Task complete.'
        ))

    def send_command(self):
        text = self.input_field.text()
        if text:
            self.chat_area.append(f'<br><span style="color: #00ffcc; font-weight: bold;">[OPERATOR]:</span> <span style="color: #ffffff;">{text}</span>')
            self.input_field.clear()
            QTimer.singleShot(600, lambda: self.chat_area.append(
                '<span style="color: #00ff66; font-weight: bold;">[JARVIS]:</span> Execution path verified. Task complete.'
            ))

    def toggle_dashboard(self):
        if self.isVisible():
            self.hide()
        else:
            self.showNormal()
            self.activateWindow()

    def closeEvent(self, event):
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.hide()
            event.ignore()
        else:
            event.accept()

class SpartanTrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setIcon(parent.cyber_icon)
        
        self.menu = QMenu()
        self.show_action = QAction("Open Command Hub")
        self.show_action.triggered.connect(self.parent().showNormal)
        self.menu.addAction(self.show_action)
        
        self.ghost_action = QAction("Toggle Dashboard")
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
    print("[DESKTOP]: Sovereign Dashboard App Online.")
    sys.exit(app.exec())
