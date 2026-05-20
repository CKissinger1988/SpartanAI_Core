import flet as ft
import os
import sys
import json
import sqlite3
import threading
import time
from datetime import datetime

# Pathing for integrated logic
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
EXPLOITS_DB = os.path.join(BACKEND_DIR, "exploits.db")

class NexusMobileApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "NEXUS // AI - MOBILE HUB"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.padding = 20
        self.page.bgcolor = "#000000"
        self.page.fonts = {
            "RobotoMono": "https://github.com/google/fonts/raw/main/apache/robotomono/RobotoMono%5Bwght%5D.ttf"
        }
        self.page.theme = ft.Theme(font_family="RobotoMono")

        self.chat_history = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
        self.status_text = ft.Text("SYSTEM STATUS: SECURE", color="#00FF00", size=12)

    def build(self):
        # Header
        header = ft.Row(
            [
                ft.Text("NEXUS // AI", size=24, color="#00FF00", weight=ft.FontWeight.BOLD),
                ft.Text("v3.2.1-MOBILE", size=12, color="#00AA00")
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        # Tabs
        tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(text="TERMINAL", icon=ft.icons.TERMINAL, content=self.terminal_view()),
                ft.Tab(text="EXPLOITS", icon=ft.icons.SECURITY, content=self.exploits_view()),
                ft.Tab(text="JARVIS", icon=ft.icons.RECORD_VOICE_OVER, content=self.jarvis_view()),
            ],
            expand=True
        )

        self.page.add(header, ft.Divider(color="#005500"), tabs, self.status_text)

    def terminal_view(self):
        self.terminal_output = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
        self.log_to_terminal("NEXUS MOBILE CORE INITIALIZED...")
        self.log_to_terminal("READY FOR UPLINK.")
        
        return ft.Container(
            content=self.terminal_output,
            padding=10,
            border=ft.border.all(1, "#005500"),
            border_radius=5,
            expand=True
        )

    def exploits_view(self):
        self.exploit_list = ft.ListView(expand=True, spacing=10)
        self.refresh_exploits()
        
        return ft.Column(
            [
                ft.Text("WEAPONIZED EXPLOIT DATABASE", color="#00FF00", size=16),
                ft.ElevatedButton("REFRESH DB", on_click=lambda _: self.refresh_exploits(), color="#000000", bgcolor="#00FF00"),
                self.exploit_list
            ],
            expand=True
        )

    def jarvis_view(self):
        self.chat_input = ft.TextField(
            hint_text="SAY SOMETHING OR TYPE COMMAND...",
            border_color="#00FF00",
            focused_border_color="#00AA00",
            color="#00FF00",
            expand=True,
            on_submit=lambda e: self.send_message(e.control.value)
        )

        return ft.Column(
            [
                self.chat_history,
                ft.Row(
                    [
                        self.chat_input,
                        ft.IconButton(icon=ft.icons.MIC, icon_color="#00FF00", on_click=lambda _: self.start_voice()),
                        ft.IconButton(icon=ft.icons.SEND, icon_color="#00FF00", on_click=lambda _: self.send_message(self.chat_input.value)),
                    ]
                )
            ],
            expand=True
        )

    def log_to_terminal(self, text):
        self.terminal_output.controls.append(
            ft.Text(f"[{datetime.now().strftime('%H:%M:%S')}]> {text}", color="#00FF00", size=12)
        )
        self.page.update()

    def refresh_exploits(self):
        self.exploit_list.controls.clear()
        if not os.path.exists(EXPLOITS_DB):
            self.exploit_list.controls.append(ft.Text("DATABASE NOT FOUND", color="#FF0000"))
        else:
            try:
                conn = sqlite3.connect(EXPLOITS_DB)
                cursor = conn.cursor()
                cursor.execute("SELECT cve_id, name, type FROM exploits LIMIT 20")
                for r in cursor.fetchall():
                    self.exploit_list.controls.append(
                        ft.ListTile(
                            title=ft.Text(f"{r[0]} - {r[1]}", color="#00FF00"),
                            subtitle=ft.Text(r[2], color="#00AA00"),
                            leading=ft.Icon(ft.icons.BUG_REPORT, color="#00FF00")
                        )
                    )
                conn.close()
            except Exception as e:
                self.exploit_list.controls.append(ft.Text(f"ERROR: {str(e)}", color="#FF0000"))
        self.page.update()

    def send_message(self, text):
        if not text: return
        self.chat_history.controls.append(ft.Text(f"[OPERATOR]> {text}", color="#00AA00"))
        self.chat_input.value = ""
        self.page.update()
        
        # Simulate Jarvis Response
        time.sleep(0.5)
        response = f"JARVIS: COMMAND '{text}' RECEIVED. EXECUTING WITH ROOT AUTHORITY."
        self.chat_history.controls.append(ft.Text(f"[{response}]", color="#00FF00"))
        self.page.update()

    def start_voice(self):
        # Flet Voice recognition implementation placeholder
        self.send_message("SPOKEN COMMAND DETECTED")

def main(page: ft.Page):
    app = NexusMobileApp(page)
    app.build()

if __name__ == "__main__":
    ft.app(target=main)
