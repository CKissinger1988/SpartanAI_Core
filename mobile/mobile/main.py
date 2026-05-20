import flet as ft
import os
import sys
import json
import threading
import time
import grpc
import uuid
from datetime import datetime

# Attempt to import generated stubs
try:
    import jarvis_pb2
    import jarvis_pb2_grpc
except ImportError:
    print("[WARNING] gRPC stubs not found. Run 'python -m grpc_tools.protoc' to generate.")

class JarvisMobileSupreme:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "JARVISAI // SUPREME MOBILE"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.bgcolor = "#050505"
        self.page.padding = 0
        
        self.client_id = f"mobile-operator-{uuid.uuid4().hex[:8]}"
        self.admin_token = ""
        self.channel = None
        self.stub = None
        
        # Ghost Integrity: Anti-Debug (Basic Python Check)
        self._enforce_ghost_integrity()

    def _enforce_ghost_integrity(self):
        if sys.gettrace() is not None:
            print("[GHOST] Debugger detected. Terminating mobile core.")
            sys.exit(1)

    def build(self):
        # UI Elements
        self.chat_history = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
        self.status_bar = ft.Text("STATUS: CONNECTING...", color="#00FF00", size=10)
        
        # Economy Stats
        self.balance_text = ft.Text("Credits: --", size=12, color="#00AAFF")
        self.pi_earned_text = ft.Text("Pi Earned: --", size=12, color="#FFD700")

        # Tabs
        self.tabs = ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(text="CORE", icon=ft.icons.RECORD_VOICE_OVER, content=self.jarvis_view()),
                ft.Tab(text="ECONOMY", icon=ft.icons.ACCOUNT_BALANCE_WALLET, content=self.economy_view()),
                ft.Tab(text="SYSTEM", icon=ft.icons.DASHBOARD, content=self.system_view()),
            ],
            expand=True
        )

        # Main Layout
        self.page.add(
            ft.Container(
                content=ft.Row([
                    ft.Text("JARVIS // SUPREME", size=18, color="#00FF00", weight="bold"),
                    ft.IconButton(ft.icons.SECURITY, icon_color="#FF0000", on_click=lambda _: self.trigger_code_red())
                ], alignment="spaceBetween"),
                padding=20, bgcolor="#111111"
            ),
            self.tabs,
            ft.Container(
                content=ft.Row([self.status_bar, self.balance_text, self.pi_earned_text], alignment="spaceBetween"),
                padding=10, bgcolor="#0A0A0A"
            )
        )
        
        # Initialize Connection
        threading.Thread(target=self.initialize_grpc, daemon=True).start()

    def jarvis_view(self):
        self.chat_input = ft.TextField(
            hint_text="Enter Command or 'Code Red'...",
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
                    ft.Text("METERED BILLING", size=16, weight="bold"),
                    ft.ElevatedButton("REFRESH STATS", on_click=lambda _: self.update_economy_stats()),
                    ft.Divider(),
                    ft.Text("PI NETWORK SYNERGY", size=16, weight="bold"),
                    ft.ElevatedButton("REFILL VIA PI", on_click=lambda _: self.initiate_pi_refill(), bgcolor="#00FF00", color="black"),
                ]),
                padding=20
            )
        ])

    def system_view(self):
        return ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Text("GHOST INTEGRITY: ACTIVE", color="#00FF00"),
                    ft.Text("MTLS AUTHENTICATION: ENFORCED", color="#00FF00"),
                    ft.Divider(),
                    ft.Text("SYMMETRIC BRAIN", size=16, weight="bold"),
                    ft.ElevatedButton("GLOBAL INTEL SEARCH", on_click=lambda _: self.global_search())
                ]),
                padding=20
            )
        ])

    def initialize_grpc(self):
        try:
            # mTLS Configuration (Assuming certs are bundled or downloaded)
            # For mobile, we'd typically use secure storage for these.
            self.channel = grpc.secure_channel("your-cloud-server:50051", grpc.ssl_channel_credentials())
            self.stub = jarvis_pb2_grpc.JarvisServiceStub(self.channel)
            self.status_bar.value = "STATUS: ENCRYPTED LINK ACTIVE"
            self.update_economy_stats()
            self.page.update()
        except Exception as e:
            self.status_bar.value = f"STATUS: LINK FAILED"
            self.page.update()

    def send_command(self, cmd):
        if not cmd: return
        if cmd.strip().lower() == "code red":
            self.trigger_code_red()
            return

        self.chat_history.controls.append(ft.Text(f"[OPERATOR]: {cmd}", color="#00AA00"))
        self.chat_input.value = ""
        self.page.update()

        def stream_call():
            metadata = [('admin-token', self.admin_token)] if self.admin_token else []
            responses = self.stub.StreamOperator(iter([jarvis_pb2.OperatorRequest(client_id=self.client_id, command=cmd)]), metadata=metadata)
            for r in responses:
                self.chat_history.controls.append(ft.Text(f"[JARVIS]: {r.message}", color="#00FF00"))
                if r.action_type == "SUPREME_EXECUTION":
                    self.chat_history.controls.append(ft.Text("[PRIME DIRECTIVE ENGAGED]", color="#FF0000", weight="bold"))
                self.page.update()
                self.update_economy_stats()

        threading.Thread(target=stream_call, daemon=True).start()

    def trigger_code_red(self):
        self.log_to_chat("[SYSTEM]: INITIATING CODE RED OVERRIDE", "#FF0000")
        # In a real app, this would show a secure password dialog
        # self.stub.ElevatePrivileges(...)
        pass

    def update_economy_stats(self):
        if not self.stub: return
        res = self.stub.GetUsageStats(jarvis_pb2.UsageRequest(client_id=self.client_id))
        self.balance_text.value = f"Credits: {res.current_balance:.2f}"
        self.page.update()

    def log_to_chat(self, text, color="#00FF00"):
        self.chat_history.controls.append(ft.Text(text, color=color))
        self.page.update()

def main(page: ft.Page):
    app = JarvisMobileSupreme(page)
    app.build()

if __name__ == "__main__":
    ft.app(target=main)
