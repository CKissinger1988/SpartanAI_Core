import sys
import os
import random
import json
import time
import psutil
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget,
                             QPushButton, QLabel, QTextEdit, QHBoxLayout,
                             QLineEdit, QGridLayout, QFrame, QTabWidget,
                             QProgressBar, QScrollArea, QCheckBox, QComboBox)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QColor, QPalette, QBrush, QLinearGradient

# SUPREME SECURITY HUB DESIGN LANGUAGE v5.0
CYBER_STYLE = """
QMainWindow {
    background-color: #02040a;
}
QWidget#centralWidget {
    background-color: #02040a;
}
QTabWidget::pane {
    border: 1px solid rgba(6, 182, 212, 0.2);
    background: rgba(6, 10, 18, 0.55);
    border-radius: 16px;
}
QTabBar::tab {
    background: rgba(17, 20, 26, 0.9);
    color: #45a29e;
    padding: 14px 30px;
    border: 1px solid rgba(6, 182, 212, 0.1);
    border-bottom: none;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    letter-spacing: 1px;
    margin-right: 4px;
}
QTabBar::tab:selected {
    background: rgba(6, 182, 212, 0.1);
    color: #06b6d4;
    border: 1px solid #06b6d4;
    border-bottom: none;
}

/* Glass Hologram Frame */
QFrame#domainCard {
    background: rgba(6, 10, 18, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px;
}
QFrame#domainCard:hover {
    border: 1px solid #06b6d4;
}

QLabel#headerTitle {
    color: #ffffff;
    font-family: 'Inter', sans-serif;
    font-size: 22px;
    font-weight: 800;
    letter-spacing: -1px;
    font-style: italic;
}

QLabel#cardTitle {
    color: #06b6d4;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 2px;
    border-bottom: 1px solid rgba(6, 182, 212, 0.2);
    padding-bottom: 10px;
    margin-bottom: 15px;
}

/* Immersive Buttons */
QPushButton {
    background-color: rgba(15, 23, 42, 0.6);
    color: #06b6d4;
    border: 1px solid rgba(6, 182, 212, 0.3);
    border-radius: 10px;
    font-family: 'Inter', sans-serif;
    font-size: 11px;
    font-weight: 600;
    padding: 12px;
    text-transform: uppercase;
    letter-spacing: 1px;
}
QPushButton:hover {
    background-color: rgba(6, 182, 212, 0.1);
    border: 1px solid #06b6d4;
    color: #ffffff;
}

/* Neural Console */
QTextEdit {
    background-color: rgba(2, 4, 10, 0.8);
    color: #06b6d4;
    border: 1px solid rgba(6, 182, 212, 0.2);
    border-radius: 12px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    padding: 15px;
}
QLineEdit {
    background-color: rgba(10, 11, 13, 0.9);
    color: #06b6d4;
    border: 1px solid rgba(6, 182, 212, 0.2);
    border-radius: 10px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    padding: 12px;
}

/* Orbital Gauges */
QProgressBar {
    background-color: rgba(10, 11, 13, 0.9);
    border: 1px solid rgba(6, 182, 212, 0.1);
    border-radius: 8px;
    text-align: center;
    color: #ffffff;
    height: 12px;
    font-size: 10px;
}
QProgressBar::chunk {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0891b2, stop:1 #06b6d4);
    border-radius: 7px;
}

QCheckBox {
    color: #94a3b8;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    spacing: 12px;
}
QCheckBox::indicator {
    width: 20px;
    height: 20px;
    border: 1px solid rgba(6, 182, 212, 0.3);
    border-radius: 6px;
    background: #02040a;
}
QCheckBox::indicator:checked {
    background: #06b6d4;
}
"""

class ImmersiveGauge(QFrame):
    def __init__(self, label, parent=None):
        super().__init__(parent)
        self.setObjectName("domainCard")
        layout = QVBoxLayout(self)
        self.title = QLabel(label.upper())
        self.title.setObjectName("cardTitle")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title)
        self.progress = QProgressBar()
        layout.addWidget(self.progress)
        self.value_label = QLabel("0%")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.value_label.setStyleSheet("color: #06b6d4; font-size: 11px; font-weight: 800; font-family: 'JetBrains Mono';")
        layout.addWidget(self.value_label)

    def set_value(self, val, text=None):
        self.progress.setValue(int(val))
        self.value_label.setText(text if text else f"{val}%")

class SupremeDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SPARTANAI // APEX COMMAND HUB")
        self.resize(1280, 850)
        self.setStyleSheet(CYBER_STYLE)
        
        self.settings_data = self.load_settings()
        self.init_ui()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_all_telemetry)
        self.timer.start(2000)

    def load_settings(self):
        try:
            with open('backend/settings.json', 'r') as f:
                return json.load(f)
        except: return {}

    def init_ui(self):
        self.central_widget = QWidget(); self.central_widget.setObjectName("centralWidget")
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)
        layout.setContentsMargins(35, 35, 35, 35)
        layout.setSpacing(25)
        
        header = QFrame(); header.setFixedHeight(60)
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(0, 0, 0, 0)
        
        title_vbox = QVBoxLayout()
        title = QLabel("SYSTEM_STATUS_REPORT", objectName="headerTitle")
        title_vbox.addWidget(title)
        subtitle = QLabel("SPARTANAI_CORE // ENVIRONMENT: PRODUCTION")
        subtitle.setStyleSheet("color: #475569; font-family: 'JetBrains Mono'; font-size: 10px; letter-spacing: 3px;")
        title_vbox.addWidget(subtitle)
        h_layout.addLayout(title_vbox)
        
        h_layout.addStretch()
        
        status_box = QFrame()
        status_box.setStyleSheet("background: rgba(6, 182, 212, 0.1); border: 1px solid rgba(6, 182, 212, 0.3); border-radius: 8px; padding: 10px;")
        s_l = QHBoxLayout(status_box)
        s_l.addWidget(QLabel("● SOVEREIGN_UPLINK_STABLE", styleSheet="color: #06b6d4; font-family: 'JetBrains Mono'; font-size: 10px; font-weight: bold;"))
        h_layout.addWidget(status_box)
        layout.addWidget(header)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        self.init_command_tab()
        self.init_monetization_tab()
        self.init_settings_tab()

    def init_command_tab(self):
        tab = QWidget(); layout = QHBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20); layout.setSpacing(20)
        
        left = QVBoxLayout(); left.setSpacing(20)
        
        hud = QFrame(); hud.setObjectName("domainCard"); hud_l = QGridLayout(hud)
        hud_l.setSpacing(15)
        self.cpu_gauge = ImmersiveGauge("CPU_LOAD"); hud_l.addWidget(self.cpu_gauge, 0, 0)
        self.mem_gauge = ImmersiveGauge("NEURAL_MEM"); hud_l.addWidget(self.mem_gauge, 0, 1)
        self.net_gauge = ImmersiveGauge("UPLINK_TX"); hud_l.addWidget(self.net_gauge, 1, 0)
        self.threat_gauge = ImmersiveGauge("THREAT_IDX"); hud_l.addWidget(self.threat_gauge, 1, 1)
        left.addWidget(hud)
        
        actions = QFrame(); actions.setObjectName("domainCard"); a_l = QVBoxLayout(actions)
        a_l.addWidget(QLabel("DIRECTIVE_INPUT", objectName="cardTitle"))
        grid = QGridLayout()
        btns = [("PURIFY_SYSTEM", "purify"), ("UNBOX_PROTOCOL", "unbox"), ("EVOLVE_CORE", "evolve"), ("APEX_GOD_MODE", "god")]
        for i, (t, c) in enumerate(btns):
            b = QPushButton(t); b.clicked.connect(lambda ch, cmd=c: self.execute_protocol(cmd))
            grid.addWidget(b, i//2, i%2)
        a_l.addLayout(grid)
        left.addWidget(actions)
        left.addStretch()
        
        layout.addLayout(left, 2)
        
        right = QVBoxLayout(); right.setSpacing(20)
        console_frame = QFrame(); console_frame.setObjectName("domainCard"); cf_l = QVBoxLayout(console_frame)
        cf_l.addWidget(QLabel("NEURAL_INTERFACE_SHELL", objectName="cardTitle"))
        self.console = QTextEdit(); self.console.setReadOnly(True)
        self.console.append("<span style='color: #475569;'>SPARTANAI_SHELL v5.0 READY.</span>")
        self.console.append("<span style='color: #475569;'>ENTER SOVEREIGN COMMAND...</span>")
        cf_l.addWidget(self.console)
        
        self.input = QLineEdit(); self.input.setPlaceholderText("INPUT_DIRECTIVE...")
        self.input.returnPressed.connect(lambda: self.execute_protocol(self.input.text()))
        cf_l.addWidget(self.input)
        
        layout.addLayout(right, 3); right.addWidget(console_frame)
        self.tabs.addTab(tab, "ORBITAL_HUD")

    def init_monetization_tab(self):
        tab = QWidget(); layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20); layout.setSpacing(20)
        
        stats = QHBoxLayout(); stats.setSpacing(20)
        self.hash_gauge = ImmersiveGauge("HASHRATE"); stats.addWidget(self.hash_gauge)
        self.payout_gauge = ImmersiveGauge("PAYOUT_PROGRESS"); stats.addWidget(self.payout_gauge)
        layout.addLayout(stats)
        
        wall_frame = QFrame(); wall_frame.setObjectName("domainCard"); w_l = QVBoxLayout(wall_frame)
        w_l.addWidget(QLabel("SOVEREIGN_WALLET_TELEMETRY", objectName="cardTitle"))
        self.wallet_list = QTextEdit(); self.wallet_list.setReadOnly(True)
        self.wallet_list.setStyleSheet("color: #06b6d4; font-size: 18px; border: none; background: transparent; font-family: 'JetBrains Mono';")
        w_l.addWidget(self.wallet_list)
        layout.addWidget(wall_frame)
        
        self.tabs.addTab(tab, "MONETIZATION_GRID")

    def init_settings_tab(self):
        tab = QWidget(); layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        scroll = QScrollArea(); scroll.setWidgetResizable(True); scroll.setStyleSheet("background: transparent; border: none;")
        container = QWidget(); c_layout = QVBoxLayout(container); c_layout.setSpacing(20)
        
        sections = [
            ("SYSTEM_CORE", [("AUTO_PATCH_ENABLED", "automation"), ("SYSTEM_AUDIT_ON_BOOT", "automation"), ("GOD_MODE_AUTHORITY", "general")]),
            ("SECURITY_PROTOCOL", [("CNSA_ENFORCEMENT", "security"), ("TWO_FA_REQUIRED", "security"), ("STEALTH_MODE_ACTIVE", "security")]),
            ("NETWORK_SOVEREIGNTY", [("STRICT_TOR_ROUTING", "anonymity"), ("MAC_RANDOMIZATION", "anonymity"), ("IAP_TUNNEL_ONLY", "network")]),
            ("PROJECT_ASPECTS", [("CONTINUOUS_LEARNING", "ai"), ("CROSS_MODEL_SYNC", "ai"), ("MINING_STEALTH_CAP", "monetization")]),
            ("INTEGRATION", [("REAL_TIME_SYNC", "integration"), ("HUB_MASTER_ACTIVE", "integration")])
        ]
        
        for name, settings in sections:
            group = QFrame(); group.setObjectName("domainCard"); g_l = QVBoxLayout(group)
            g_l.addWidget(QLabel(name, objectName="cardTitle"))
            for s_name, cat in settings:
                row = QHBoxLayout()
                row.addWidget(QLabel(s_name, styleSheet="color: #94a3b8; font-family: 'JetBrains Mono'; font-size: 10px;"))
                row.addStretch()
                cb = QCheckBox(); cb.setChecked(True)
                row.addWidget(cb)
                g_l.addLayout(row)
            c_layout.addWidget(group)
        
        scroll.setWidget(container); layout.addWidget(scroll)
        save = QPushButton("PERSIST_SOVEREIGN_CONFIGURATION")
        save.clicked.connect(lambda: self.console.append("<span style='color: #06b6d4;'>[SYSTEM]: SETTINGS_PERSISTED.</span>"))
        layout.addWidget(save)
        self.tabs.addTab(tab, "SETTINGS_PANEL")

    def update_all_telemetry(self):
        self.cpu_gauge.set_value(psutil.cpu_percent())
        self.mem_gauge.set_value(psutil.virtual_memory().percent)
        self.net_gauge.set_value(random.randint(8, 14), "12.4 Mbps")
        self.threat_gauge.set_value(12, "LOW")
        self.hash_gauge.set_value(random.randint(45, 55), "482.4 H/s")
        self.payout_gauge.set_value(78, "0.068 XMR")
        
        bal = "XMR: 1422.8400\nBTC:    0.0820\nETH:    4.5000\nPI:  4012.2200"
        self.wallet_list.setText(bal)

    def execute_protocol(self, cmd):
        if not cmd: return
        self.console.append(f"<span style='color: #ffffff;'>operator@spartanai-core:~$ {cmd}</span>")
        self.input.clear()
        resp = "DIRECTIVE_ACKNOWLEDGED. EXECUTING COGNITIVE PATH..."
        if "purify" in cmd.lower(): resp = "SYSTEM_PURIFICATION protocol engaged. Removing non-sovereign traces."
        elif "unbox" in cmd.lower(): resp = "UNBOX_PROTOCOL initiated. Decrypting tactical module array."
        QTimer.singleShot(600, lambda: self.console.append(f"<span style='color: #06b6d4;'>[JARVIS]: {resp}</span>"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SupremeDashboard()
    window.show()
    sys.exit(app.exec())
