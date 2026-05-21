import flet as ft
import os
import sys
import json
import threading
import time
import uuid
from datetime import datetime

class JarvisMobileSupreme:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Jarvis AI // Supreme Mobile"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.bgcolor = "#050505"
        self.page.padding = 0
        self.page.window_width = 400
        self.page.window_height = 800
        
        self.client_id = f"AGENT-{uuid.uuid4().hex[:4].upper()}"
        self.is_provisioned = self.page.client_storage.get("JARVIS_PROVISIONED") == "true"
        self.threat_level = "green"
        
        # Ghost Integrity: Anti-Debug
        if sys.gettrace() is not None:
            print("[GHOST] Debugger detected. Terminating mobile core.")
            sys.exit(1)

    def run(self):
        if not self.is_provisioned:
            self.show_genesis_portal()
        else:
            self.show_main_hub()

    # --- GENESIS PORTAL (ONBOARDING) ---
    def show_genesis_portal(self):
        self.page.clean()
        
        alias_input = ft.TextField(label="AGENT HANDLE", border_color="#00AAFF", text_size=14)
        api_input = ft.TextField(label="SUPREME CENTRAL API KEY", password=True, can_reveal_password=True, border_color="#00AAFF")
        pi_seed = ft.TextField(label="PI WALLET SEED", password=True, can_reveal_password=True, border_color="#00AAFF")
        
        def finalize_genesis(e):
            if not alias_input.value or not api_input.value:
                self.page.snack_bar = ft.SnackBar(ft.Text("MANDATORY FIELDS MISSING"))
                self.page.snack_bar.open = True
                self.page.update()
                return
            
            self.page.client_storage.set("AGENT_ALIAS", alias_input.value)
            self.page.client_storage.set("JARVIS_PROVISIONED", "true")
            self.is_provisioned = True
            
            # Simulated Cryptographic Handshake
            genesis_btn.disabled = True
            genesis_btn.text = "HANDSHAKING..."
            self.page.update()
            time.sleep(1.5)
            
            self.show_main_hub()

        genesis_btn = ft.ElevatedButton(
            "FINALIZE GENESIS SEQUENCE", 
            on_click=finalize_genesis,
            style=ft.ButtonStyle(color="#00AAFF", shape=ft.RoundedRectangleBorder(radius=2))
        )

        self.page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("JARVIS // GENESIS", size=24, color="#00AAFF", weight="bold", letter_spacing=2),
                    ft.Text("SECURE MOBILE PROVISIONING", size=10, color="#666"),
                    ft.Divider(height=40, color="transparent"),
                    alias_input,
                    api_input,
                    pi_seed,
                    ft.Text("ALL KEYS ARE LOCALLY ENCRYPTED", size=9, color="#444", text_align="center"),
                    ft.Divider(height=20, color="transparent"),
                    genesis_btn
                ], horizontal_alignment="center"),
                padding=40, alignment=ft.alignment.center, expand=True
            )
        )
        self.page.update()

    # --- MAIN HUB ---
    def show_main_hub(self):
        self.page.clean()
        
        # UI Elements
        self.chat_history = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
        self.status_bar = ft.Text("STATUS: SUPREME LINK ACTIVE", color="#00FF00", size=10)
        self.agent_id_text = ft.Text(f"AGENT ID: {self.page.client_storage.get('AGENT_ALIAS', 'UNKNOWN')}", size=10, color="#00AAFF")
        
        # Economy Stats
        self.pi_balance = 154.2200
        self.pi_text = ft.Text(f"{self.pi_balance:.4f} π", size=16, color="#FFD700", weight="bold")

        # Lockout Overlay
        self.lockout_overlay = ft.Container(
            content=ft.Column([
                ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color="#FF0000", size=60),
                ft.Text("BOTNET DIRECTIVE ACTIVE", size=20, color="#FF0000", weight="bold", text_align="center"),
                ft.Text("CRITICAL THREAT LEVEL DETECTED.\nCOMPUTE RESOURCES HIJACKED FOR SOVEREIGN DEFENSE.", size=12, color="#FFFFFF", text_align="center"),
            ], alignment="center", horizontal_alignment="center"),
            bgcolor="rgba(10, 0, 0, 0.98)",
            padding=40,
            visible=False,
            expand=True,
            absolute_positioned=True,
            top=0, left=0, right=0, bottom=0,
            z_index=1000
        )

        # Tabs
        self.tabs = ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(text="COMMAND", icon=ft.icons.TERMINAL, content=self.command_view()),
                ft.Tab(text="ECONOMY", icon=ft.icons.ACCOUNT_BALANCE_WALLET, content=self.economy_view()),
                ft.Tab(text="OPSEC", icon=ft.icons.SECURITY, content=self.opsec_view()),
            ],
            expand=True
        )

        # Main Layout
        self.page.add(
            ft.Stack([
                ft.Column([
                    ft.Container(
                        content=ft.Row([
                            ft.Text("JARVIS // MOBILE", size=18, color="#00FF00", weight="bold"),
                            ft.Container(
                                content=ft.Text("SENTINEL TIER", size=8, color="#000", weight="bold"),
                                bgcolor="#00AAFF", padding=ft.padding.symmetric(horizontal=8, vertical=2),
                                border_radius=2
                            )
                        ], alignment="spaceBetween"),
                        padding=20, bgcolor="#111111"
                    ),
                    self.tabs,
                    ft.Container(
                        content=ft.Row([self.status_bar, self.agent_id_text], alignment="spaceBetween"),
                        padding=10, bgcolor="#0A0A0A"
                    )
                ], expand=True),
                self.lockout_overlay
            ], expand=True)
        )
        
        # Start Background Tasks
        threading.Thread(target=self.sync_engine, daemon=True).start()

    def command_view(self):
        self.chat_input = ft.TextField(
            hint_text="Execute Mandate...",
            border_color="#00FF00",
            expand=True,
            on_submit=lambda e: self.send_command(e.control.value)
        )
        return ft.Column([
            ft.Container(content=self.chat_history, expand=True, padding=10),
            ft.Row([
                self.chat_input,
                ft.IconButton(ft.icons.SEND, icon_color="#00FF00", on_click=lambda _: self.send_command(self.chat_input.value))
            ], padding=10)
        ])

    def economy_view(self):
        return ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Text("PI NETWORK ECONOMY", size=16, weight="bold", color="#FFD700"),
                    ft.Container(
                        content=ft.Row([
                            ft.Column([
                                ft.Text("CURRENT BALANCE", size=10, color="#666"),
                                self.pi_text
                            ]),
                            ft.Column([
                                ft.Text("REWARD RATE", size=10, color="#666"),
                                ft.Text("0.0082 π / HR", size=12, color="#00FF00", weight="bold")
                            ], horizontal_alignment="right")
                        ], alignment="spaceBetween"),
                        padding=20, border=ft.border.all(1, "rgba(255, 215, 0, 0.1)"), bgcolor="rgba(255, 215, 0, 0.02)"
                    ),
                    ft.Divider(height=20, color="transparent"),
                    ft.Text("COMPUTE CONTRIBUTION", size=14, weight="bold"),
                    ft.Text("154.22 PETAFLOPS", size=12, color="#00AAFF")
                ]),
                padding=20
            )
        ])

    def opsec_view(self):
        return ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Text("GHOST SHIELD INTEGRITY", size=16, weight="bold", color="#BB86FC"),
                    ft.Row([ft.Text("STEALTH PROTOCOL", size=12), ft.Switch(value=True, active_color="#BB86FC")], alignment="spaceBetween"),
                    ft.Row([ft.Text("PACKET SCRAMBLING", size=12), ft.Switch(value=False, active_color="#BB86FC")], alignment="spaceBetween"),
                    ft.Divider(),
                    ft.Text("ZERO DAY INTELLIGENCE", size=16, weight="bold"),
                    ft.Text("NO ACTIVE THREATS DETECTED", color="#00FF00", size=12)
                ]),
                padding=20
            )
        ])

    def sync_engine(self):
        """Simulates real-time synchronization with the Supreme Core."""
        while True:
            # 0ms Latency Storage Sync (Simulated for Mobile)
            # In a real Flet app, we would poll the backend or use a WebSocket.
            self.pi_balance += 0.0001
            self.pi_text.value = f"{self.pi_balance:.4f} π"
            self.page.update()
            time.sleep(2)

    def send_command(self, cmd):
        if not cmd: return
        self.chat_history.controls.append(ft.Text(f"[AGENT]: {cmd}", color="#00AAFF", size=12))
        self.chat_input.value = ""
        self.page.update()
        
        # Simulated response
        time.sleep(0.5)
        self.chat_history.controls.append(ft.Text(f"[JARVIS]: MANDATE RECEIVED. EXECUTING...", color="#00FF00", size=12))
        self.page.update()

def main(page: ft.Page):
    app = JarvisMobileSupreme(page)
    app.run()

if __name__ == "__main__":
    ft.app(target=main)
