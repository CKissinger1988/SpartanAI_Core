import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QTextEdit, QHBoxLayout, QLineEdit
from PySide6.QtCore import Qt, QPoint, QSize
from PySide6.QtGui import QMouseEvent, QFont

class GhostWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SentinelAI - Ghost")
        
        # Transparent, Frameless, Draggable
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.expanded = False
        self.oldPos = self.pos()
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        # Ghost Toggle Button
        self.toggle_btn = QPushButton("??")
        self.toggle_btn.setFixedSize(50, 50)
        self.toggle_btn.setStyleSheet("background-color: rgba(20, 20, 20, 180); color: #00ffcc; border-radius: 25px; font-size: 24px;")
        self.toggle_btn.clicked.connect(self.toggle_dashboard)
        self.layout.addWidget(self.toggle_btn)
        
        # Dashboard Container
        self.dashboard_container = QWidget()
        self.dash_layout = QVBoxLayout(self.dashboard_container)
        self.dash_layout.setContentsMargins(5, 5, 5, 5)
        
        # Streamlabs-style Chatbox Aesthetics
        # High contrast, minimal borders, transparent background, stylized text
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
        self.input_field.setStyleSheet("background-color: rgba(20, 20, 20, 200); color: #00ffcc; border: none; border-bottom: 2px solid #00ffcc; font-family: 'Segoe UI'; font-size: 12px; padding: 5px;")
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
        self.resize(350, 400) if self.expanded else self.resize(60, 60)
        self.snap_to_bottom_right()

if __name__ == "__main__":
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)
    ghost = GhostWidget()
    ghost.show()
    sys.exit(app.exec())
