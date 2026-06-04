import sys
import os
import random
import json
import time
import math
import psutil
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget,
                             QPushButton, QLabel, QTextEdit, QHBoxLayout,
                             QLineEdit, QGridLayout, QFrame, QStackedWidget,
                             QProgressBar, QScrollArea, QCheckBox, QListWidget,
                             QListWidgetItem, QSizePolicy)
from PySide6.QtCore import Qt, QTimer, QSize, QUrl
from PySide6.QtGui import QFont, QColor, QIcon, QPainter, QLinearGradient, QPen, QPainterPath
from PySide6.QtWebEngineWidgets import QWebEngineView

# SUPREME SPARTANAI COMMAND CENTER v6.0 // ABSOLUTE SOVEREIGNTY
CYBER_STYLE = """
QMainWindow {
    background-color: #02040a;
}
QWidget#centralWidget {
    background-color: #02040a;
}
QFrame#sidePanel {
    background-color: rgba(6, 10, 18, 0.9);
    border-right: 1px solid rgba(6, 182, 212, 0.2);
}
QListWidget {
    background-color: transparent;
    border: none;
    outline: none;
}
QListWidget::item {
    color: #94a3b8;
    padding: 18px 25px;
    border-left: 3px solid transparent;
    font-family: 'Inter', sans-serif;
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
}
QListWidget::item:selected {
    color: #06b6d4;
    background-color: rgba(6, 182, 212, 0.1);
    border-left: 3px solid #06b6d4;
}
QListWidget::item:hover {
    background-color: rgba(6, 182, 212, 0.05);
}

QFrame#domainCard {
    background: rgba(6, 10, 18, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 20px;
    padding: 20px;
}
QFrame#domainCard:hover {
    border: 1px solid rgba(6, 182, 212, 0.4);
}

QLabel#headerTitle {
    color: #ffffff;
    font-family: 'Inter', sans-serif;
    font-size: 26px;
    font-weight: 900;
    letter-spacing: -1px;
    font-style: italic;
}

QLabel#cardTitle {
    color: #06b6d4;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 3px;
    border-bottom: 1px solid rgba(6, 182, 212, 0.2);
    padding-bottom: 12px;
    margin-bottom: 20px;
}

QPushButton {
    background-color: rgba(15, 23, 42, 0.6);
    color: #06b6d4;
    border: 1px solid rgba(6, 182, 212, 0.3);
    border-radius: 12px;
    font-family: 'Inter', sans-serif;
    font-size: 10px;
    font-weight: 700;
    padding: 14px;
    text-transform: uppercase;
    letter-spacing: 2px;
}
QPushButton:hover {
    background-color: rgba(6, 182, 212, 0.1);
    border: 1px solid #06b6d4;
    color: #ffffff;
}

QTextEdit {
    background-color: rgba(2, 4, 10, 0.9);
    color: #06b6d4;
    border: 1px solid rgba(6, 182, 212, 0.2);
    border-radius: 16px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    padding: 20px;
}

QProgressBar {
    background-color: rgba(10, 11, 13, 0.9);
    border: 1px solid rgba(6, 182, 212, 0.1);
    border-radius: 10px;
    text-align: center;
    color: #ffffff;
    height: 14px;
    font-size: 10px;
    font-weight: bold;
}
QProgressBar::chunk {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0891b2, stop:1 #06b6d4);
    border-radius: 9px;
}

QCheckBox {
    color: #94a3b8;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    spacing: 15px;
    letter-spacing: 1px;
}
QCheckBox::indicator {
    width: 22px;
    height: 22px;
    border: 1px solid rgba(6, 182, 212, 0.3);
    border-radius: 7px;
    background: #02040a;
}
QCheckBox::indicator:checked {
    background: #06b6d4;
}

QScrollArea {
    background: transparent;
    border: none;
}
"""

class WaveformViz(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 100)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)
        self.offset = 0
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(QColor(6, 182, 212), 2))
        path = QPainterPath()
        path.moveTo(0, 50)
        for x in range(self.width()):
            y = 50 + 25 * math.sin((x + self.offset) * 0.05)
            path.lineTo(x, y)
        painter.drawPath(path)
        self.offset += 2

class ImmersiveGauge(QFrame):
    def __init__(self, label, parent=None):
        super().__init__(parent)
        self.setObjectName("domainCard")
        layout = QVBoxLayout(self)
        self.title = QLabel(label.upper(), objectName="cardTitle")
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

class SupremeCommandCenter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SUPREME SPARTANAI COMMAND CENTER // v6.0")
        self.resize(1800, 1000)
        self.setStyleSheet(CYBER_STYLE)
        
        self.init_ui()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_telemetry)
        self.timer.start(2000)

    def init_ui(self):
        self.central_widget = QWidget(); self.central_widget.setObjectName("centralWidget")
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # LEFT SIDE PANEL
        self.side_panel = QFrame(); self.side_panel.setObjectName("sidePanel")
        self.side_panel.setFixedWidth(280)
        self.side_layout = QVBoxLayout(self.side_panel)
        self.side_layout.setContentsMargins(0, 40, 0, 40)
        
        logo_label = QLabel("SUPREME COMMAND")
        logo_label.setStyleSheet("color: #ffffff; font-family: 'Inter'; font-size: 16px; font-weight: 900; letter-spacing: 4px; padding: 0 30px; margin-bottom: 40px;")
        self.side_layout.addWidget(logo_label)
        
        self.nav_list = QListWidget()
        items = ["CORE_ORCHESTRATOR", "SECURITY_HUB", "TOUCH_TACTICAL", "TACTICAL_HUB", "MONETIZATION", "NETWORK_OPS", "AI_CORTEX", "SETTINGS"]
        for item in items:
            it = QListWidgetItem(item)
            it.setSizeHint(QSize(0, 65))
            self.nav_list.addItem(it)
        self.nav_list.currentRowChanged.connect(self.switch_tab)
        self.side_layout.addWidget(self.nav_list)
        self.side_layout.addStretch()
        
        footer_status = QLabel("● SUPREME_UPLINK: ACTIVE")
        footer_status.setStyleSheet("color: #06b6d4; font-family: 'JetBrains Mono'; font-size: 9px; font-weight: bold; padding: 20px 30px;")
        self.side_layout.addWidget(footer_status)
        
        self.main_layout.addWidget(self.side_panel)

        # RIGHT CONTENT AREA
        self.content_stack = QStackedWidget()
        self.main_layout.addWidget(self.content_stack)

        self.init_core_tab()
        self.init_security_tab()
        self.init_touch_tab()
        self.init_tactical_tab()
        self.init_monetization_tab()
        self.init_network_tab()
        self.init_ai_tab()
        self.init_settings_tab()
        
        self.nav_list.setCurrentRow(0)

    def init_core_tab(self):
        page = QWidget(); layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40); layout.setSpacing(30)
        
        header = QLabel("SYSTEM_CORE_ORCHESTRATION", objectName="headerTitle")
        layout.addWidget(header)
        
        hud_row = QHBoxLayout(); hud_row.setSpacing(25)
        
        # HUD GRID
        hud_grid = QGridLayout(); hud_grid.setSpacing(25)
        self.cpu_gauge = ImmersiveGauge("CPU_LOAD"); hud_grid.addWidget(self.cpu_gauge, 0, 0)
        self.mem_gauge = ImmersiveGauge("NEURAL_MEM"); hud_grid.addWidget(self.mem_gauge, 0, 1)
        self.net_gauge = ImmersiveGauge("UPLINK_TX"); hud_grid.addWidget(self.net_gauge, 1, 0)
        self.threat_gauge = ImmersiveGauge("THREAT_IDX"); hud_grid.addWidget(self.threat_gauge, 1, 1)
        hud_row.addLayout(hud_grid, 2)

        # CORE PROTOCOLS
        proto_frame = QFrame(); proto_frame.setObjectName("domainCard"); p_l = QVBoxLayout(proto_frame)
        p_l.addWidget(QLabel("SUPREME_PROTOCOLS", objectName="cardTitle"))
        p_btns = [("PURIFY_SYSTEM", "purify"), ("UNBOX_PROTOCOL", "unbox"), ("EVOLVE_CORE", "evolve"), ("APEX_GOD_MODE", "god")]
        for t, c in p_btns:
            btn = QPushButton(t); btn.clicked.connect(lambda ch, cmd=c: self.execute_protocol(cmd))
            p_l.addWidget(btn)
        hud_row.addWidget(proto_frame, 1)
        layout.addLayout(hud_row)
        
        # CONSOLE
        console_frame = QFrame(); console_frame.setObjectName("domainCard"); cf_l = QVBoxLayout(console_frame)
        cf_l.addWidget(QLabel("NEURAL_INTERFACE_SHELL", objectName="cardTitle"))
        self.console = QTextEdit(); self.console.setReadOnly(True)
        self.console.append("<span style='color: #475569;'>SUPREME_COMMAND_CENTER v6.0 READY.</span>")
        cf_l.addWidget(self.console)
        
        input_row = QHBoxLayout()
        self.input = QLineEdit(); self.input.setPlaceholderText("INPUT_DIRECTIVE...")
        self.input.returnPressed.connect(lambda: self.execute_protocol(self.input.text()))
        input_row.addWidget(self.input)
        cf_l.addLayout(input_row)
        
        layout.addWidget(console_frame, 1)
        self.content_stack.addWidget(page)

    def init_security_tab(self):
        page = QWidget(); layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://34.182.160.186:9091"))
        layout.addWidget(self.browser)
        self.content_stack.addWidget(page)

    def init_touch_tab(self):
        page = QWidget(); layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40); layout.setSpacing(30)
        layout.addWidget(QLabel("TOUCH_TACTICAL_INTERFACE", objectName="headerTitle"))
        
        viz_container = QFrame(); viz_container.setObjectName("domainCard")
        v_l = QVBoxLayout(viz_container)
        v_l.addWidget(WaveformViz(), alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(viz_container)

        grid = QGridLayout(); grid.setSpacing(20)
        btns = [("SYS STATUS", "systems status"), ("NET RECON", "analyze network"), 
                ("DEPLOY MESH", "deploy_mesh"), ("ISO SECURE", "encrypt_iso"), 
                ("S.T.E.P.P.", "stepp_audit"), ("SYNC BRAIN", "sync_brain")]
        
        for i, (text, cmd) in enumerate(btns):
            btn = QPushButton(text)
            btn.setStyleSheet("height: 100px; font-size: 14px; border: 2px solid #06b6d4;")
            btn.clicked.connect(lambda checked, c=cmd: self.execute_protocol(c))
            grid.addWidget(btn, i // 2, i % 2)
        
        layout.addLayout(grid)
        layout.addStretch()
        self.content_stack.addWidget(page)

    def init_tactical_tab(self):
        page = QWidget(); layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40); layout.setSpacing(30)
        layout.addWidget(QLabel("SUPREME_TACTICAL_TOOLKIT", objectName="headerTitle"))
        
        grid = QGridLayout(); grid.setSpacing(25)
        tools = [
            ("EXPLOIT_MANAGER", "Tactical vulnerability research & payload delivery", "python backend/exploit_manager.py"),
            ("IOT_INFILTRATOR", "Smart device discovery and lateral movement", "python backend/iot_manager.py"),
            ("NEURAL_GAME_ENGINE", "Simulated tactical environment for agent training", "python backend/game_manager.py"),
            ("IDENTITY_VAULT", "Sovereign credential management & encryption", "python backend/user_manager.py")
        ]
        
        for i, (name, desc, cmd) in enumerate(tools):
            card = QFrame(); card.setObjectName("domainCard"); c_l = QVBoxLayout(card)
            c_l.addWidget(QLabel(name, styleSheet="color: #06b6d4; font-weight: 800; font-size: 14px;"))
            c_l.addWidget(QLabel(desc, styleSheet="color: #475569; font-size: 11px; margin-bottom: 10px;"))
            btn = QPushButton("LAUNCH_MODULE")
            btn.clicked.connect(lambda ch, c=cmd: os.system(f"start cmd /k {c}"))
            c_l.addWidget(btn)
            grid.addWidget(card, i//2, i%2)
            
        layout.addLayout(grid); layout.addStretch()
        self.content_stack.addWidget(page)

    def init_monetization_tab(self):
        page = QWidget(); layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40); layout.setSpacing(30)
        layout.addWidget(QLabel("MONETIZATION_AND_RESOURCE_HARVESTING", objectName="headerTitle"))
        
        stats = QHBoxLayout(); stats.setSpacing(25)
        self.hash_gauge = ImmersiveGauge("HASHRATE"); stats.addWidget(self.hash_gauge)
        self.payout_gauge = ImmersiveGauge("PAYOUT_PROGRESS"); stats.addWidget(self.payout_gauge)
        layout.addLayout(stats)
        
        wall_frame = QFrame(); wall_frame.setObjectName("domainCard"); w_l = QVBoxLayout(wall_frame)
        w_l.addWidget(QLabel("SOVEREIGN_WALLET_MATRIX", objectName="cardTitle"))
        self.wallet_list = QTextEdit(); self.wallet_list.setReadOnly(True)
        self.wallet_list.setStyleSheet("color: #06b6d4; font-size: 24px; border: none; background: transparent; font-family: 'JetBrains Mono'; line-height: 1.5;")
        w_l.addWidget(self.wallet_list)
        layout.addWidget(wall_frame)
        self.content_stack.addWidget(page)

    def init_network_tab(self):
        page = QWidget(); layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40); layout.setSpacing(30)
        layout.addWidget(QLabel("NETWORK_SOVEREIGNTY_OPS", objectName="headerTitle"))
        grid = QGridLayout(); grid.setSpacing(20)
        ops = [("STRICT_TOR_ROUTING", "Enforce 100% .onion exit nodes"),
               ("MAC_RANDOMIZATION", "Rotate system hardware signatures"),
               ("IAP_TUNNEL_FORCE", "Hyper-isolated Google IAP tunnel"),
               ("VPN_CHAINS", "Multi-hop sovereign VPN sequence")]
        for i, (name, desc) in enumerate(ops):
            card = QFrame(); card.setObjectName("domainCard"); c_l = QVBoxLayout(card)
            c_l.addWidget(QLabel(name, styleSheet="color: #06b6d4; font-weight: 800; font-size: 12px;"))
            c_l.addWidget(QLabel(desc, styleSheet="color: #475569; font-size: 10px;"))
            cb = QCheckBox("ACTIVE"); cb.setChecked(True); c_l.addWidget(cb)
            grid.addWidget(card, i//2, i%2)
        layout.addLayout(grid); layout.addStretch()
        self.content_stack.addWidget(page)

    def init_ai_tab(self):
        page = QWidget(); layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40); layout.setSpacing(30)
        layout.addWidget(QLabel("NEURAL_CORTEX_SETTINGS", objectName="headerTitle"))
        card = QFrame(); card.setObjectName("domainCard"); c_l = QVBoxLayout(card)
        c_l.addWidget(QLabel("COGNITIVE_SHARD_STATUS", objectName="cardTitle"))
        shards = ["JARVIS_SUPREME (Active)", "ANTIGRAVITY_GOOD (Active)", "GEMINI_QUESTIONABLE (Active)", "GROK_EVIL (Active)"]
        for s in shards:
            row = QHBoxLayout()
            row.addWidget(QLabel(s, styleSheet="color: #94a3b8; font-family: 'JetBrains Mono';"))
            row.addStretch()
            row.addWidget(QLabel("SYNCED", styleSheet="color: #06b6d4; font-weight: bold;"))
            c_l.addLayout(row)
        layout.addWidget(card); layout.addStretch()
        self.content_stack.addWidget(page)

    def init_settings_tab(self):
        page = QWidget(); layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40); layout.setSpacing(30)
        layout.addWidget(QLabel("GLOBAL_SYSTEM_CONFIGURATION", objectName="headerTitle"))
        scroll = QScrollArea(); scroll.setWidgetResizable(True)
        container = QWidget(); c_l = QVBoxLayout(container); c_l.setSpacing(25)
        sections = [("AUTOMATION", ["AUTO_PATCH", "BOOT_AUDIT"]), ("SECURITY", ["CNSA_ENFORCE", "TWO_FA"]), ("MONETIZATION", ["STEALTH_MINING", "AUTOSWAP"]), ("INTEGRATION", ["REAL_TIME_SYNC", "HUB_MASTER_INTEGRATED"])]
        for name, items in sections:
            group = QFrame(); group.setObjectName("domainCard"); g_l = QVBoxLayout(group)
            g_l.addWidget(QLabel(name, objectName="cardTitle"))
            for item in items:
                row = QHBoxLayout(); row.addWidget(QLabel(item, styleSheet="color: #94a3b8; font-family: 'JetBrains Mono';"))
                row.addStretch(); cb = QCheckBox(); cb.setChecked(True); row.addWidget(cb); g_l.addLayout(row)
            c_l.addWidget(group)
        scroll.setWidget(container); layout.addWidget(scroll)
        sync_btn = QPushButton("EXECUTE LIVE SYNC (CORE + HUB MASTER)")
        sync_btn.clicked.connect(lambda: os.system("powershell -ExecutionPolicy Bypass -File scripts/live_sync.ps1"))
        layout.addWidget(sync_btn)
        self.content_stack.addWidget(page)

    def switch_tab(self, index):
        self.content_stack.setCurrentIndex(index)

    def update_telemetry(self):
        self.cpu_gauge.set_value(psutil.cpu_percent())
        self.mem_gauge.set_value(psutil.virtual_memory().percent)
        self.net_gauge.set_value(random.randint(8, 18), f"{random.randint(10, 20)} Mbps")
        self.threat_gauge.set_value(random.randint(5, 15), "LOW")
        self.hash_gauge.set_value(random.randint(45, 60), f"{random.randint(480, 550)} H/s")
        self.payout_gauge.set_value(random.randint(70, 85), f"0.{random.randint(6, 9)}8 XMR")
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
    window = SupremeCommandCenter()
    window.show()
    sys.exit(app.exec())
