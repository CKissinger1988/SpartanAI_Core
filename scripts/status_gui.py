import flet as ft
import random
import time

def main(page: ft.Page):
    page.title = "NEXUS // AI // TACTICAL INTERFACE"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0a0a0a"

    # Status indicators
    status_text = ft.Text("SYSTEMS NOMINAL", color=ft.colors.GREEN_400, weight=ft.FontWeight.BOLD)
    
    # Progress bars
    def create_metric(name):
        return ft.Column([
            ft.Text(name, color=ft.colors.CYAN_400, size=12),
            ft.ProgressBar(value=random.random(), color=ft.colors.GREEN_400, bgcolor=ft.colors.GREY_900)
        ])

    metrics = ft.Column([
        create_metric("READ/WRITE SPEED"),
        create_metric("SYSTEM LOAD"),
        create_metric("MEMORY USAGE"),
        create_metric("DATABASE SIZE")
    ])

    page.add(
        ft.Text("NEXUS // AI // TACTICAL STATUS", color=ft.colors.CYAN_400, size=20, weight=ft.FontWeight.BOLD),
        status_text,
        ft.Divider(),
        metrics
    )

ft.app(target=main)
