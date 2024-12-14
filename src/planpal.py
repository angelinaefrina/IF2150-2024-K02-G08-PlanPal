import flet as ft
from utils.buttons import *
from pages.manage_event import EventManagerApp
from pages.landing import LandingApp  # Import LandingPage
from database.database import Database 
from database.database import EventDatabase
from database.database import GuestListDatabase
from database.database import BudgetDatabase
from database.database import VendorDatabase
from database.database import RundownDatabase

# class PlanPal:
#     def __init__(self, page):
#         self.page = page
#         self.page.title = "PLANPAL"

#         # Center the text using a Container with alignment
#         self.page.add(
#             ft.Container(
#                 content=ft.Text("Welcome to PlanPal!"),
#                 alignment=ft.alignment.center
#             )
#         )

#         # Add buttons
#         self.page.add(
#             ft.Container(
#                 content=ft.Column(
#                     controls=[
#                         ft.ElevatedButton(text="Manage Events", on_click=self.open_manage_event),
#                         ft.ElevatedButton(text="Go to Landing Page", on_click=self.open_landing_page)  # Add button to open landing page
#                     ],
#                     alignment=ft.MainAxisAlignment.CENTER,
#                     horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#                     spacing=10
#                 ),
#                 alignment=ft.alignment.center
#             )
#         )

#     def open_manage_event(self, e):
#         # Clear the current page content
#         self.page.controls.clear()
#         # Initialize and display the EventManagerApp
#         EventManagerApp(self.page)
#         self.page.update()

#     def open_landing_page(self, e):
#         # Clear the current page content
#         self.page.controls.clear()
#         # Initialize and display the LandingPage
#         LandingApp(self.page)
#         self.page.update()

def main(page: ft.Page):
    app = LandingApp(page)

ft.app(target=main)