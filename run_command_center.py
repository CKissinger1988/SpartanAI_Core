import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from backend.supreme_command_center import SupremeCommandCenter
from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SupremeCommandCenter()
    window.show()
    sys.exit(app.exec())
