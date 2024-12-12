import flet as ft
from utils.buttons import *
from pages.manage_event import EventManagerApp

class PlanPal:
    def __init__(self, page):
        self.page = page
        self.page.title = "PLANPAL"

        # Center the text using a Container with alignment
        self.page.add(
            ft.Container(
                content=ft.Text("Welcome to PlanPal!"),
                alignment=ft.alignment.center
            )
        )

        # Add buttons
        self.page.add(
            ft.Container(
                content=ft.ElevatedButton(text="Manage Events", on_click=self.open_manage_event),
                alignment=ft.alignment.center
            )
        )

    def open_manage_event(self, e):
        # Clear the current page content
        self.page.controls.clear()
        # Initialize and display the EventManagerApp
        EventManagerApp(self.page)
        self.page.update()

def main(page: ft.Page):
    app = PlanPal(page)

ft.app(target=main)