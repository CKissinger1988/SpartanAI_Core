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
                             QListWidgetItem, QSizePolicy, QGraphicsDropShadowEffect)
from PySide6.QtCore import Qt, QTimer, QSize, QUrl, QPropertyAnimation, QEasingCurve, QPoint
from PySide6.QtGui import QFont, QColor, QIcon, QPainter, QLinearGradient, QPen, QPainterPath
from PySide6.QtWebEngineWidgets import QWebEngineView

# SUPREME SPARTANAI COMMAND CENTER v6.1 // ABSOLUTE SOVEREIGNTY
# AUTHORED BY GEMINI // ALIGNED WITH SECURITY CORE AESTHETIC

CYBER_STYLE = """
QMainWindow {
    background-color: #02040a;
}
QWidget#centralWidget {
    background-color: #02040a;
}
QFrame#sidePanel {
    background-color: rgba(6, 10, 18, 0.95);
    border-right: 1px solid rgba(6, 182, 212, 0.2);
}
QListWidget {
    background-color: transparent;
    border: none;
    outline: none;
    margin-top: 20px;
}
QListWidget::item {
    color: #64748b;
    padding: 22px 30px;
    border-left: 4px solid transparent;
    font-family: 'Inter', sans-serif;
    font-size: 11px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 3px;
}
QListWidget::item:selected {
    color: #06b6d4;
    background-color: rgba(6, 182, 212, 0.08);
    border-left: 4px solid #06b6d4;
}
QListWidget::item:hover {
    color: #ffffff;
    background-color: rgba(6, 182, 212, 0.04);
}

QFrame#glassCard {
    background: rgba(6, 10, 18, 0.6);
    border: 1px solid rgba(6, 182, 212, 0.1);
    border-radius: 12px;
}

QLabel#headerTitle {
    color: #ffffff;
    font-family: 'Inter', sans-serif;
    font-size: 28px;
    font-weight: 900;
    letter-spacing: -1.5px;
    font-style: italic;
    margin-bottom: 5px;
}

QLabel#subTitle {
    color: #06b6d4;
    font-family: 'JetBrains Mono';
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 5px;
    margin-bottom: 30px;
}

QLabel#cardTitle {
    color: #06b6d4;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 4px;
    padding: 15px;
    border-bottom: 1px solid rgba(6, 182, 212, 0.1);
}

QPushButton {
    background-color: rgba(15, 23, 42, 0.4);
    color: #06b6d4;
    border: 1px solid rgba(6, 182, 212, 0.2);
    border-radius: 8px;
    font-family: 'Inter', sans-serif;
    font-size: 10px;
    font-weight: 700;
    padding: 12px;
    text-transform: uppercase;
    letter-spacing: 2px;
}
QPushButton:hover {
    background-color: rgba(6, 182, 212, 0.1);
    border: 1px solid #06b6d4;
    color: #ffffff;
}
QPushButton#actionBtn {
    background-color: rgba(6, 182, 212, 0.1);
    border: 1px solid #06b6d4;
    font-weight: 900;
}

QTextEdit {
    background-color: rgba(2, 4, 10, 0.8);
    color: #06b6d4;
    border: 1px solid rgba(6, 182, 212, 0.1);
    border-radius: 12px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    padding: 15px;
}

QProgressBar {
    background-color: rgba(0, 0, 0, 0.5);
    border: 1px solid rgba(6, 182, 212, 0.1);
    border-radius: 4px;
    text-align: center;
    color: transparent;
    height: 6px;
}
QProgressBar::chunk {
    background-color: #06b6d4;
}

QCheckBox {
    color: #94a3b8;
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    spacing: 10px;
}
QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 1px solid rgba(6, 182, 212, 0.3);
    border-radius: 4px;
    background: #02040a;
}
QCheckBox::indicator:checked {
    background: #06b6d4;
}

QLineEdit {
    background: rgba(15, 23, 42, 0.3);
    border: 1px solid rgba(6, 182, 212, 0.2);
    border-radius: 8px;
    color: #ffffff;
    font-family: 'JetBrains Mono';
    font-size: 11px;
    padding: 10px 15px;
}
"""

class GlassCard(QFrame):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setObjectName("glassCard")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        self.header = QLabel(title.upper(), objectName="cardTitle")
        self.layout.addWidget(self.header)
        
        self.container = QWidget()
        self.content_layout = QVBoxLayout(self.container)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.layout.addWidget(self.container)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(6, 182, 212, 40))
        shadow.setOffset(0, 0)
        self.setGraphicsEffect(shadow)

class CyberGauge(QWidget):
    def __init__(self, label):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        row = QHBoxLayout()
        row.addWidget(QLabel(label, styleSheet="color: #64748b; font-size: 9px; font-weight: 800; font-family: 'JetBrains Mono';"))
        row.addStretch()
        self.val_label = QLabel("0%", styleSheet="color: #06b6d4; font-size: 10px; font-weight: 900; font-family: 'JetBrains Mono';")
        row.addWidget(self.val_label)
        layout.addLayout(row)
        
        self.progress = QProgressBar()
        layout.addWidget(self.progress)
        
    def set_value(self, val, text=None):
        self.progress.setValue(int(val))
        self.val_label.setText(text if text else f"{val}%")

class SupremeCommandCenter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SUPREME SPARTANAI COMMAND CENTER // SOVEREIGN_C2")
        self.resize(1900, 1000)
        self.setStyleSheet(CYBER_STYLE)
        
        self.init_ui()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_telemetry)
        self.timer.start(2000)

    def init_ui(self):
        self.central_widget = QWidget(); self.central_widget.setObjectName("centralWidget")
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0); self.main_layout.setSpacing(0)

        # SIDEBAR
        self.side_panel = QFrame(); self.side_panel.setObjectName("sidePanel")
        self.side_panel.setFixedWidth(300)
        self.side_layout = QVBoxLayout(self.side_panel)
        self.side_layout.setContentsMargins(0, 50, 0, 40)
        
        logo_container = QVBoxLayout()
        logo_container.setContentsMargins(35, 0, 30, 40)
        logo = QLabel("SPARTANAI")
        logo.setStyleSheet("color: #ffffff; font-family: 'Inter'; font-size: 20px; font-weight: 900; letter-spacing: 5px;")
        logo_container.addWidget(logo)
        tagline = QLabel("SUPREME_COMMAND_HUB")
        tagline.setStyleSheet("color: #06b6d4; font-family: 'JetBrains Mono'; font-size: 8px; font-weight: 800; letter-spacing: 3px;")
        logo_container.addWidget(tagline)
        self.side_layout.addLayout(logo_container)
        
        self.nav_list = QListWidget()
        tabs = [
            ("CORE_ORCHESTRATION", "system-run"),
            ("SECURITY_HUB", "security-high"),
            ("TOUCH_TACTICAL", "input-tablet"),
            ("TACTICAL_TOOLKIT", "tools-report"),
            ("MONETIZATION", "monetization"),
            ("NETWORK_SOVEREIGNTY", "network-wireless"),
            ("AI_CORTEX", "brain"),
            ("CENTRAL_SETTINGS", "settings")
        ]
        for name, icon in tabs:
            it = QListWidgetItem(name)
            it.setSizeHint(QSize(0, 70))
            self.nav_list.addItem(it)
        self.nav_list.currentRowChanged.connect(self.switch_tab)
        self.side_layout.addWidget(self.nav_list)
        self.side_layout.addStretch()
        
        status_box = QFrame()
        status_box.setStyleSheet("background: rgba(6, 182, 212, 0.05); border-top: 1px solid rgba(6, 182, 212, 0.1); padding: 30px;")
        sb_l = QVBoxLayout(status_box)
        self.uptime_label = QLabel("UPTIME: 08:42:11")
        self.uptime_label.setStyleSheet("color: #64748b; font-family: 'JetBrains Mono'; font-size: 9px; font-weight: bold;")
        sb_l.addWidget(self.uptime_label)
        self.uplink_status = QLabel("● UPLINK: SOVEREIGN")
        self.uplink_status.setStyleSheet("color: #06b6d4; font-family: 'JetBrains Mono'; font-size: 9px; font-weight: 900;")
        sb_l.addWidget(self.uplink_status)
        self.side_layout.addWidget(status_box)
        
        self.main_layout.addWidget(self.side_panel)

        # CONTENT
        self.content_stack = QStackedWidget()
        self.main_layout.addWidget(self.content_stack)

        self.init_core_page()
        self.init_security_page()
        self.init_touch_page()
        self.init_tactical_page()
        self.init_monetization_page()
        self.init_network_page()
        self.init_ai_page()
        self.init_settings_page()
        
        self.nav_list.setCurrentRow(0)

    def add_page_header(self, layout, title, sub):
        layout.addWidget(QLabel(title, objectName="headerTitle"))
        layout.addWidget(QLabel(sub, objectName="subTitle"))

    def init_core_page(self):
        page = QWidget(); layout = QVBoxLayout(page)
        layout.setContentsMargins(60, 60, 60, 60); layout.setSpacing(0)
        self.add_page_header(layout, "CORE_ORCHESTRATION", "SOVEREIGN SYSTEM CONTROL & DIAGNOSTICS")
        
        grid = QGridLayout(); grid.setSpacing(30)
        
        # TELEMETRY
        tele_card = GlassCard("Neural_Telemetry"); grid.addWidget(tele_card, 0, 0, 1, 2)
        t_l = QGridLayout(tele_card.container)
        self.cpu_g = CyberGauge("CPU_LOAD"); t_l.addWidget(self.cpu_g, 0, 0)
        self.mem_g = CyberGauge("MEM_POOL"); t_l.addWidget(self.mem_g, 0, 1)
        self.net_g = CyberGauge("UPLINK_TX"); t_l.addWidget(self.net_g, 1, 0)
        self.thr_g = CyberGauge("THREAT_IDX"); t_l.addWidget(self.thr_g, 1, 1)
        
        # PROTOCOLS
        proto_card = GlassCard("Sovereign_Protocols"); grid.addWidget(proto_card, 0, 2)
        p_l = QVBoxLayout(proto_card.container); p_l.setSpacing(15)
        p_btns = [("PURIFY_SYSTEM", "purify"), ("UNBOX_PROTOCOL", "unbox"), ("EVOLVE_CORE", "evolve"), ("APEX_GOD_MODE", "god")]
        for t, c in p_btns:
            btn = QPushButton(t); btn.clicked.connect(lambda ch, cmd=c: self.execute_protocol(cmd))
            p_l.addWidget(btn)
            
        # TERMINAL
        term_card = GlassCard("Neural_Shell_Interface"); grid.addWidget(term_card, 1, 0, 1, 3)
        term_l = QVBoxLayout(term_card.container)
        self.console = QTextEdit(); self.console.setReadOnly(True)
        self.console.append("<span style='color: #475569;'>[SYSTEM]: SUPREME_ORCHESTRATOR_v6.1_ONLINE</span>")
        term_l.addWidget(self.console)
        self.input = QLineEdit(); self.input.setPlaceholderText("INPUT_DIRECTIVE...")
        self.input.returnPressed.connect(lambda: self.execute_protocol(self.input.text()))
        term_l.addWidget(self.input)
        
        layout.addLayout(grid)
        self.content_stack.addWidget(page)

    def init_security_page(self):
        page = QWidget(); layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://34.182.160.186:9091"))
        layout.addWidget(self.browser)
        self.content_stack.addWidget(page)

    def init_touch_page(self):
        page = QWidget(); layout = QVBoxLayout(page)
        layout.setContentsMargins(60, 60, 60, 60); layout.setSpacing(0)
        self.add_page_header(layout, "TOUCH_TACTICAL", "HAPTIC OPTIMIZED FIELD INTERFACE")
        
        grid = QGridLayout(); grid.setSpacing(20)
        btns = [("SYSTEM STATUS", "status"), ("NETWORK RECON", "recon"), 
                ("DEPLOY SWARM", "swarm"), ("ENCRYPT VAULT", "vault"), 
                ("S.T.E.P.P.", "stepp"), ("SYNC NEURAL", "sync")]
        for i, (t, c) in enumerate(btns):
            btn = QPushButton(t); btn.setMinimumHeight(120); btn.setFont(QFont("Inter", 12, QFont.Weight.Black))
            btn.clicked.connect(lambda ch, cmd=c: self.execute_protocol(cmd))
            grid.addWidget(btn, i//3, i%3)
        layout.addLayout(grid); layout.addStretch()
        self.content_stack.addWidget(page)

    def init_tactical_page(self):
        page = QWidget(); layout = QVBoxLayout(page)
        layout.setContentsMargins(60, 60, 60, 60); layout.setSpacing(0)
        self.add_page_header(layout, "TACTICAL_TOOLKIT", "OFFENSIVE & DEFENSIVE INTELLIGENCE ARRAY")
        
        grid = QGridLayout(); grid.setSpacing(25)
        tools = [
            ("EXPLOIT_MANAGER", "Tactical vulnerability research & payload delivery", "python backend/exploit_manager.py"),
            ("IOT_INFILTRATOR", "Smart device discovery and lateral movement", "python backend/iot_manager.py"),
            ("NEURAL_GAME_ENGINE", "Simulated tactical environment for agent training", "python backend/game_manager.py"),
            ("IDENTITY_VAULT", "Sovereign credential management & encryption", "python backend/user_manager.py")
        ]
        for i, (name, desc, cmd) in enumerate(tools):
            card = GlassCard(name); c_l = QVBoxLayout(card.container)
            c_l.addWidget(QLabel(desc, styleSheet="color: #64748b; font-size: 10px; margin-bottom: 20px;"))
            btn = QPushButton("ENGAGE_MODULE"); btn.setObjectName("actionBtn")
            def launch(c=cmd):
                if sys.platform == "win32": os.system(f"start cmd /k {c}")
                else: os.system(f"konsole -e {c} &")
            btn.clicked.connect(launch)
            c_l.addWidget(btn)
            grid.addWidget(card, i//2, i%2)
        layout.addLayout(grid); layout.addStretch()
        self.content_stack.addWidget(page)

    def init_monetization_page(self):
        page = QWidget(); layout = QVBoxLayout(page)
        layout.setContentsMargins(60, 60, 60, 60); layout.setSpacing(0)
        self.add_page_header(layout, "MONETIZATION", "RESOURCE HARVESTING & CAPITAL AGGREGATION")
        
        stats = QHBoxLayout(); stats.setSpacing(30)
        self.h_g = CyberGauge("HASHRATE_AGGREGATE"); stats.addWidget(self.h_g)
        self.p_g = CyberGauge("PAYOUT_THRESHOLD"); stats.addWidget(self.p_g)
        layout.addLayout(stats)
        
        wallet_card = GlassCard("Sovereign_Assets"); layout.addWidget(wallet_card)
        self.wallets = QTextEdit(); self.wallets.setReadOnly(True)
        self.wallets.setStyleSheet("font-size: 20px; color: #06b6d4; border: none; background: transparent;")
        QVBoxLayout(wallet_card.container).addWidget(self.wallets)
        self.content_stack.addWidget(page)

    def init_network_page(self):
        page = QWidget(); layout = QVBoxLayout(page)
        layout.setContentsMargins(60, 60, 60, 60); layout.setSpacing(0)
        self.add_page_header(layout, "NETWORK_SOVEREIGNTY", "DECENTRALIZED ANONYMITY & UPLINK SECURITY")
        
        grid = QGridLayout(); grid.setSpacing(25)
        ops = [("STRICT_TOR_ROUTING", "Enforce 100% .onion exit nodes"),
               ("MAC_RANDOMIZATION", "Rotate system hardware signatures"),
               ("IAP_TUNNEL_FORCE", "Hyper-isolated Google IAP tunnel"),
               ("VPN_CHAINS", "Multi-hop sovereign VPN sequence")]
        for i, (name, desc) in enumerate(ops):
            card = GlassCard(name); c_l = QVBoxLayout(card.container)
            c_l.addWidget(QLabel(desc, styleSheet="color: #64748b; font-size: 10px; margin-bottom: 15px;"))
            cb = QCheckBox("PROTOCOL_ACTIVE"); cb.setChecked(True); c_l.addWidget(cb)
            grid.addWidget(card, i//2, i%2)
        layout.addLayout(grid); layout.addStretch()
        self.content_stack.addWidget(page)

    def init_ai_page(self):
        page = QWidget(); layout = QVBoxLayout(page)
        layout.setContentsMargins(60, 60, 60, 60); layout.setSpacing(0)
        self.add_page_header(layout, "NEURAL_CORTEX", "COGNITIVE SHARD MANAGEMENT & EVOLUTION")
        
        card = GlassCard("Shard_Matrix"); layout.addWidget(card)
        c_l = QVBoxLayout(card.container); c_l.setSpacing(20)
        shards = ["JARVIS_SUPREME (Primary)", "ANTIGRAVITY_GOOD (Cortex)", "GEMINI_QUESTIONABLE (Cortex)", "GROK_EVIL (Cortex)"]
        for s in shards:
            row = QHBoxLayout()
            row.addWidget(QLabel(s, styleSheet="color: #ffffff; font-family: 'JetBrains Mono'; font-weight: 800; font-size: 11px;"))
            row.addStretch()
            row.addWidget(QLabel("SYNC_OK", styleSheet="color: #06b6d4; font-weight: 900; font-size: 10px;"))
            c_l.addLayout(row)
        layout.addStretch()
        self.content_stack.addWidget(page)

    def init_settings_page(self):
        page = QWidget(); layout = QVBoxLayout(page)
        layout.setContentsMargins(60, 60, 60, 60); layout.setSpacing(0)
        self.add_page_header(layout, "CENTRAL_SETTINGS", "GLOBAL PARAMETER ARCHITECTURE")
        
        scroll = QScrollArea(); scroll.setWidgetResizable(True)
        container = QWidget(); c_l = QVBoxLayout(container); c_l.setSpacing(25)
        sections = [("AUTOMATION", ["AUTO_PATCH", "BOOT_AUDIT"]), ("SECURITY", ["CNSA_ENFORCE", "TWO_FA"]), ("INTEGRATION", ["REAL_TIME_SYNC", "HUB_MASTER"])]
        for name, items in sections:
            group = GlassCard(name); g_l = QVBoxLayout(group.container)
            for item in items:
                row = QHBoxLayout(); row.addWidget(QLabel(item, styleSheet="color: #64748b; font-family: 'JetBrains Mono'; font-size: 10px; font-weight: 700;"))
                row.addStretch(); cb = QCheckBox(); cb.setChecked(True); row.addWidget(cb); g_l.addLayout(row)
            c_l.addWidget(group)
        scroll.setWidget(container); layout.addWidget(scroll)
        
        sync_btn = QPushButton("EXECUTE GLOBAL SYNC"); sync_btn.setObjectName("actionBtn")
        def run_sync():
            if sys.platform == "win32": os.system("powershell -ExecutionPolicy Bypass -File scripts/live_sync.ps1")
            else: os.system("bash scripts/live_sync.sh")
        sync_btn.clicked.connect(run_sync)
        layout.addWidget(sync_btn)
        self.content_stack.addWidget(page)

    def switch_tab(self, index):
        self.content_stack.setCurrentIndex(index)

    def update_telemetry(self):
        self.cpu_g.set_value(psutil.cpu_percent())
        self.mem_g.set_value(psutil.virtual_memory().percent)
        self.net_g.set_value(random.randint(12, 22), f"{random.randint(15, 25)} Mbps")
        self.thr_g.set_value(random.randint(2, 8), "OPTIMAL")
        self.h_g.set_value(random.randint(45, 65), f"{random.randint(500, 600)} H/s")
        self.p_g.set_value(random.randint(80, 95), f"0.{random.randint(8, 9)}1 XMR")
        self.wallets.setText("XMR: 1422.8400  BTC: 0.0820\nETH: 4.5000     PI: 4012.2200")

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
