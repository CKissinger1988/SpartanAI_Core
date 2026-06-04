import sys
import os
import random
import json
import time
import math
import psutil
import subprocess
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget,
                             QPushButton, QLabel, QTextEdit, QHBoxLayout,
                             QLineEdit, QGridLayout, QFrame, QStackedWidget,
                             QProgressBar, QScrollArea, QCheckBox, QListWidget,
                             QListWidgetItem, QSizePolicy, QGraphicsDropShadowEffect,
                             QComboBox)
from PySide6.QtCore import Qt, QTimer, QSize, QUrl, QProcess, QRect
from PySide6.QtGui import QFont, QColor, QIcon, QPainter, QLinearGradient, QPen, QPainterPath
from PySide6.QtWebEngineWidgets import QWebEngineView

# SUPREME SPARTANAI COMMAND CENTER v7.0 // FINALITY UNIFIED
# AUTHORED BY GEMINI // ASCENSION ABSOLUTE

class Theme:
    CYAN = "#06b6d4"
    AMBER = "#f59e0b"
    RED = "#ef4444"
    BG = "#02040a"
    SIDEBAR = "rgba(6, 10, 18, 0.95)"
    CARD = "rgba(6, 10, 18, 0.6)"
    TEXT = "#94a3b8"

    def __init__(self):
        self.color = self.CYAN
        self.glow = "rgba(6, 182, 212, 0.15)"
        self.glow_heavy = "rgba(6, 182, 212, 0.35)"

    def set_level(self, level):
        if level == "MEDIUM":
            self.color = self.AMBER
            self.glow = "rgba(245, 158, 11, 0.15)"
            self.glow_heavy = "rgba(245, 158, 11, 0.35)"
        elif level == "HIGH" or level == "CRITICAL":
            self.color = self.RED
            self.glow = "rgba(239, 68, 68, 0.15)"
            self.glow_heavy = "rgba(239, 68, 68, 0.35)"
        else:
            self.color = self.CYAN
            self.glow = "rgba(6, 182, 212, 0.15)"
            self.glow_heavy = "rgba(6, 182, 212, 0.35)"

GLOBAL_THEME = Theme()

def get_cyber_style():
    color = GLOBAL_THEME.color
    return f"""
    QMainWindow {{ background-color: #02040a; }}
    QWidget#centralWidget {{ background-color: #02040a; }}
    QFrame#sidePanel {{
        background-color: {GLOBAL_THEME.SIDEBAR};
        border-right: 1px solid {color}33;
    }}
    QListWidget::item {{
        color: #64748b; padding: 22px 30px; border-left: 4px solid transparent;
        font-family: 'Inter'; font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 3px;
    }}
    QListWidget::item:selected {{
        color: {color}; background-color: {color}14; border-left: 4px solid {color};
    }}
    QFrame#glassCard {{
        background: {GLOBAL_THEME.CARD};
        border: 1px solid {color}1a;
        border-radius: 12px;
    }}
    QLabel#headerTitle {{
        color: #ffffff; font-family: 'Inter'; font-size: 32px; font-weight: 900; letter-spacing: -1.5px; font-style: italic;
    }}
    QLabel#subTitle {{
        color: {color}; font-family: 'JetBrains Mono'; font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 5px;
    }}
    QLabel#cardTitle {{
        color: {color}; font-family: 'JetBrains Mono'; font-size: 10px; font-weight: 800; text-transform: uppercase; letter-spacing: 4px;
        padding: 15px; border-bottom: 1px solid {color}1a;
    }}
    QPushButton {{
        background-color: #0f172a66; color: {color}; border: 1px solid {color}33; border-radius: 8px;
        font-family: 'Inter'; font-size: 10px; font-weight: 700; padding: 12px; text-transform: uppercase;
    }}
    QPushButton:hover {{ background-color: {color}1a; border: 1px solid {color}; color: #ffffff; }}
    QTextEdit {{ background-color: #02040a; color: {color}; border: 1px solid {color}1a; border-radius: 12px; font-family: 'JetBrains Mono'; }}
    QProgressBar {{ background-color: #000000; border: 1px solid {color}1a; border-radius: 4px; height: 6px; }}
    QProgressBar::chunk {{ background-color: {color}; }}
    QLineEdit {{ background: #0f172a4d; border: 1px solid {color}33; border-radius: 8px; color: #ffffff; font-family: 'JetBrains Mono'; padding: 10px; }}
    """

class WaveformViz(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(60)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(50)
        self.offset = 0
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        color = QColor(GLOBAL_THEME.color)
        painter.setPen(QPen(color, 2))
        path = QPainterPath()
        center_y = self.height() // 2
        path.moveTo(0, center_y)
        for x in range(self.width()):
            y = center_y + (self.height() // 3) * math.sin((x + self.offset) * 0.05) * random.uniform(0.8, 1.2)
            path.lineTo(x, y)
        painter.drawPath(path)
        self.offset += 2

class ImmersiveGauge(QFrame):
    def __init__(self, label, parent=None):
        super().__init__(parent)
        self.setObjectName("glassCard")
        self.setMinimumHeight(100)
        layout = QVBoxLayout(self)
        self.title = QLabel(label.upper())
        self.title.setStyleSheet(f"color: {GLOBAL_THEME.color}; font-size: 9px; font-weight: 800; font-family: 'JetBrains Mono';")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title)
        self.progress = QProgressBar()
        layout.addWidget(self.progress)
        self.value_label = QLabel("0%")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.value_label.setStyleSheet(f"color: white; font-size: 11px; font-weight: 800; font-family: 'JetBrains Mono';")
        layout.addWidget(self.value_label)

    def set_value(self, val, text=None):
        self.progress.setValue(int(val))
        self.value_label.setText(text if text else f"{val}%")

class GlassCard(QFrame):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setObjectName("glassCard")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.header = QLabel(title.upper(), objectName="cardTitle")
        self.layout.addWidget(self.header)
        
        self.container = QWidget()
        self.content_layout = QVBoxLayout(self.container)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.layout.addWidget(self.container)

class SupremeCommandCenter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SUPREME SPARTANAI COMMAND CENTER // FINALITY_V7.0")
        self.resize(1800, 1000)
        self.update_style()
        
        self.gemini_process = QProcess(self)
        self.gemini_process.readyReadStandardOutput.connect(self.handle_gemini_output)
        self.gemini_process.readyReadStandardError.connect(self.handle_gemini_error)
        
        self.init_ui()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_telemetry)
        self.timer.start(1000)

    def update_style(self):
        self.setStyleSheet(get_cyber_style())

    def init_ui(self):
        self.central_widget = QWidget(); self.central_widget.setObjectName("centralWidget")
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0); self.main_layout.setSpacing(0)

        # SIDEBAR
        self.side_panel = QFrame(); self.side_panel.setObjectName("sidePanel")
        self.side_panel.setFixedWidth(320)
        self.side_layout = QVBoxLayout(self.side_panel)
        self.side_layout.setContentsMargins(0, 50, 0, 40)
        
        logo = QLabel("SPARTANAI"); logo.setStyleSheet("color: white; font-family: 'Inter'; font-size: 24px; font-weight: 900; letter-spacing: 8px; padding-left: 40px;")
        tag = QLabel("SUPREME_SYSTEM_ORCHESTRATOR"); tag.setStyleSheet(f"color: {GLOBAL_THEME.color}; font-size: 7px; font-weight: 800; letter-spacing: 3px; padding-left: 40px; margin-bottom: 40px;")
        self.side_layout.addWidget(logo); self.side_layout.addWidget(tag)
        
        self.nav_list = QListWidget()
        tabs = ["ORCHESTRATION", "SECURITY_CORE", "TOUCH_TACTICAL", "MONETIZATION", "NETWORK_MESH", "NEURAL_CORTEX", "CONFIG"]
        for name in tabs:
            it = QListWidgetItem(name); it.setSizeHint(QSize(0, 70))
            self.nav_list.addItem(it)
        self.nav_list.currentRowChanged.connect(self.switch_tab)
        self.side_layout.addWidget(self.nav_list)
        self.side_layout.addStretch()
        
        # Waveform in Sidebar
        self.side_layout.addWidget(WaveformViz())
        
        # Threat Level
        self.threat_combo = QComboBox()
        self.threat_combo.addItems(["DEFCON 5 (CYAN)", "DEFCON 3 (AMBER)", "DEFCON 1 (RED)"])
        self.threat_combo.currentIndexChanged.connect(self.change_threat_level)
        self.threat_combo.setStyleSheet("margin: 20px; height: 40px;")
        self.side_layout.addWidget(self.threat_combo)
        
        self.main_layout.addWidget(self.side_panel)

        self.content_stack = QStackedWidget()
        self.main_layout.addWidget(self.content_stack)

        self.init_orch_page()
        self.init_security_page()
        self.init_touch_page()
        self.init_monetization_page()
        self.init_network_page()
        self.init_ai_page()
        self.init_config_page()
        
        self.nav_list.setCurrentRow(0)

    def change_threat_level(self, index):
        levels = ["LOW", "MEDIUM", "HIGH"]
        GLOBAL_THEME.set_level(levels[index])
        self.update_style()

    def add_header(self, layout, title, sub):
        layout.addWidget(QLabel(title, objectName="headerTitle"))
        layout.addWidget(QLabel(sub, objectName="subTitle"))
        layout.addSpacing(20)

    def init_orch_page(self):
        page = QWidget(); layout = QVBoxLayout(page); layout.setContentsMargins(60, 60, 60, 60)
        self.add_header(layout, "CORE_ORCHESTRATION", "SOVEREIGN NEURAL INTERFACE")
        
        grid = QGridLayout(); grid.setSpacing(30)
        
        # Console
        term_card = GlassCard("Jarvis_Secure_Shell"); grid.addWidget(term_card, 0, 0, 2, 2)
        t_l = QVBoxLayout(term_card.container)
        self.console = QTextEdit(); self.console.setReadOnly(True)
        self.console.append("<span style='color: #475569;'>[SYSTEM]: SUPREME_UPLINK_ESTABLISHED. SPARTANAI_v7.0 READY.</span>")
        t_l.addWidget(self.console)
        self.input = QLineEdit(); self.input.setPlaceholderText("INPUT_DIRECTIVE (RELAY_TO_GEMINI)...")
        self.input.returnPressed.connect(lambda: self.execute_directive(self.input.text()))
        t_l.addWidget(self.input)
        
        # Telemetry Gauges
        telemetry_card = GlassCard("System_Telemetry"); grid.addWidget(telemetry_card, 0, 2)
        tem_l = QVBoxLayout(telemetry_card.container); tem_l.setSpacing(15)
        self.cpu_gauge = ImmersiveGauge("CPU_LOAD"); tem_l.addWidget(self.cpu_gauge)
        self.mem_gauge = ImmersiveGauge("NEURAL_MEM"); tem_l.addWidget(self.mem_gauge)
        self.threat_gauge = ImmersiveGauge("THREAT_IDX"); tem_l.addWidget(self.threat_gauge)
        
        # Protocols
        proto_card = GlassCard("Sovereign_Protocols"); grid.addWidget(proto_card, 1, 2)
        p_l = QVBoxLayout(proto_card.container); p_l.setSpacing(15)
        for t, c in [("PURIFY_SYSTEM", "purify"), ("UNBOX_TACTICAL", "unbox"), ("EVOLVE_CORE", "evolve"), ("GOD_MODE", "god")]:
            btn = QPushButton(t); btn.clicked.connect(lambda ch, cmd=c: self.execute_directive(cmd))
            p_l.addWidget(btn)
        
        layout.addLayout(grid)
        self.content_stack.addWidget(page)

    def init_security_page(self):
        page = QWidget(); layout = QVBoxLayout(page); layout.setContentsMargins(0, 0, 0, 0)
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://localhost:5173")) # Assuming local React dev server
        layout.addWidget(self.browser)
        self.content_stack.addWidget(page)

    def init_touch_page(self):
        page = QWidget(); layout = QVBoxLayout(page); layout.setContentsMargins(60, 60, 60, 60)
        self.add_header(layout, "TOUCH_TACTICAL", "HAPTIC_SOVEREIGN_INTERFACE")
        grid = QGridLayout(); grid.setSpacing(20)
        btns = [("SYS_STATUS", "status"), ("NET_RECON", "scan"), ("SWARM_DEPLOY", "swarm"), 
                ("VAULT_LOCK", "lock"), ("STEPP_AUDIT", "stepp"), ("NEURAL_SYNC", "sync")]
        for i, (t, c) in enumerate(btns):
            btn = QPushButton(t); btn.setMinimumHeight(120); btn.setFont(QFont("Inter", 13, QFont.Weight.Black))
            btn.clicked.connect(lambda ch, cmd=c: self.execute_directive(cmd))
            grid.addWidget(btn, i//3, i%3)
        layout.addLayout(grid); layout.addStretch()
        self.content_stack.addWidget(page)

    def init_monetization_page(self):
        page = QWidget(); layout = QVBoxLayout(page); layout.setContentsMargins(60, 60, 60, 60)
        self.add_header(layout, "MONETIZATION_MATRIX", "RESOURCE HARVESTING & CAPITAL AGGREGATION")
        
        grid = QGridLayout(); grid.setSpacing(30)
        
        stats_card = GlassCard("Harvest_Telemetry"); grid.addWidget(stats_card, 0, 0)
        s_l = QVBoxLayout(stats_card.container)
        self.hash_gauge = ImmersiveGauge("HASHRATE"); s_l.addWidget(self.hash_gauge)
        self.payout_gauge = ImmersiveGauge("PAYOUT_PROGRESS"); s_l.addWidget(self.payout_gauge)
        
        wallet_card = GlassCard("Sovereign_Wallet"); grid.addWidget(wallet_card, 0, 1)
        w_l = QVBoxLayout(wallet_card.container)
        self.wallet_display = QTextEdit(); self.wallet_display.setReadOnly(True)
        self.wallet_display.setStyleSheet("font-size: 20px; font-family: 'JetBrains Mono'; border: none;")
        w_l.addWidget(self.wallet_display)

        self.payout_btn = QPushButton("TRIGGER ON-DEMAND SWEEP")
        self.payout_btn.clicked.connect(lambda: self.execute_directive("autonomous_sweep --on-demand"))
        w_l.addWidget(self.payout_btn)
        
        layout.addLayout(grid); layout.addStretch()
        self.content_stack.addWidget(page)

    def init_network_page(self):
        page = QWidget(); layout = QVBoxLayout(page); layout.setContentsMargins(60, 60, 60, 60)
        self.add_header(layout, "NETWORK_MESH", "DECENTRALIZED ANONYMITY LAYER")
        grid = QGridLayout(); grid.setSpacing(25)
        nets = ["STRICT_TOR", "MAC_RANDOM", "IAP_TUNNEL", "VPN_CHAIN", "MESH_NODE", "C2_UPLINK"]
        for i, t in enumerate(nets):
            card = GlassCard(t); c_l = QVBoxLayout(card.container)
            cb = QCheckBox("ACTIVE"); cb.setChecked(True); c_l.addWidget(cb)
            grid.addWidget(card, i//3, i%3)
        layout.addLayout(grid); layout.addStretch()
        self.content_stack.addWidget(page)

    def init_ai_page(self):
        page = QWidget(); layout = QVBoxLayout(page); layout.setContentsMargins(60, 60, 60, 60)
        self.add_header(layout, "NEURAL_CORTEX", "COGNITIVE SHARD EVOLUTION")
        card = GlassCard("Shard_Synapse_Status"); layout.addWidget(card)
        c_l = QVBoxLayout(card.container); c_l.setSpacing(20)
        for s in ["JARVIS (Primary)", "ANTIGRAVITY (Good)", "GEMINI (Questionable)", "GROK (Evil)"]:
            row = QHBoxLayout(); row.addWidget(QLabel(s, styleSheet="font-weight: 800; font-size: 14px;"))
            row.addStretch()
            status = QLabel("SYNC_OK", styleSheet=f"color: {GLOBAL_THEME.CYAN}; font-weight: 900;")
            row.addWidget(status)
            c_l.addLayout(row)
        layout.addStretch()
        self.content_stack.addWidget(page)

    def init_config_page(self):
        page = QWidget(); layout = QVBoxLayout(page); layout.setContentsMargins(60, 60, 60, 60)
        self.add_header(layout, "CONFIG_CENTRAL", "GLOBAL PARAMETER ARCHITECTURE")
        scroll = QScrollArea(); scroll.setWidgetResizable(True); scroll.setStyleSheet("background: transparent; border: none;")
        container = QWidget(); c_l = QVBoxLayout(container); c_l.setSpacing(30)
        
        configs = [
            ("SYSTEM_CORE", ["AUTO_PATCH", "BOOT_SEC", "GOD_MODE_AUTH"]),
            ("SECURITY_PROTOCOL", ["CNSA_ENFORCE", "2FA_MANDATORY", "STEALTH_ACTIVE"]),
            ("AI_SYNAPSE", ["CONTINUOUS_LEARNING", "CROSS_MODEL_SYNC", "RAG_INJECTION"])
        ]
        
        for n, items in configs:
            g = GlassCard(n); gl = QVBoxLayout(g.container)
            for i in items:
                row = QHBoxLayout(); row.addWidget(QLabel(i)); row.addStretch()
                cb = QCheckBox(); cb.setChecked(True); row.addWidget(cb)
                gl.addLayout(row)
            c_l.addWidget(g)
            
        scroll.setWidget(container); layout.addWidget(scroll)
        self.content_stack.addWidget(page)

    def switch_tab(self, index): self.content_stack.setCurrentIndex(index)

    def update_telemetry(self):
        self.cpu_gauge.set_value(psutil.cpu_percent())
        self.mem_gauge.set_value(psutil.virtual_memory().percent)
        self.threat_gauge.set_value(15, "NOMINAL")
        
        self.hash_gauge.set_value(random.randint(48, 52), "492.8 H/s")
        self.payout_gauge.set_value(82, "0.071 XMR")
        
        self.wallet_display.setText("XMR: 1422.8400\nBTC:    0.0820\nBTC_LN: 0.1500\nETH:    4.5000")

    def execute_directive(self, cmd):
        if not cmd: return
        self.console.append(f"<span style='color: #ffffff;'>operator@spartanai-core:~$ {cmd}</span>")
        self.input.clear()
        
        # RELAY TO GEMINI CLI
        gemini_cmd = r"C:\Users\ckiss\AppData\Roaming\npm\gemini.cmd"
        if sys.platform != "win32": gemini_cmd = "gemini"
        
        args = ["-p", cmd, "--skip-trust"]
        self.console.append("<span style='color: #475569;'>[JARVIS]: RELAYING TO GEMINI_CORE...</span>")
        self.gemini_process.start(gemini_cmd, args)

    def handle_gemini_output(self):
        data = self.gemini_process.readAllStandardOutput().data().decode()
        self.console.append(f"<span style='color: {GLOBAL_THEME.color};'>{data}</span>")

    def handle_gemini_error(self):
        data = self.gemini_process.readAllStandardError().data().decode()
        if data.strip():
            self.console.append(f"<span style='color: #ef4444;'>[ERROR]: {data}</span>")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SupremeCommandCenter()
    window.show()
    sys.exit(app.exec())
