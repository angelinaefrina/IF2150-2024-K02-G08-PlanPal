import flet as ft
from utils.buttons import *
from pages.manage_event import EventManagerApp
from pages.landing import LandingApp  # Import LandingPage
from database.database import EventDatabase, GuestListDatabase, BudgetDatabase, VendorDatabase, RundownDatabase  # Import all databases

class PlanPal:
    def __init__(self, page):
        self.page = page
        self.page.title = "PLANPAL"

        # Initialize the databases
        self.event_db = EventDatabase("planpal.db")
        self.event_db.create_event_table()

        self.guest_list_db = GuestListDatabase("planpal.db")
        self.guest_list_db.create_guest_list_table()
        self.budget_db = BudgetDatabase("planpal.db")
        self.budget_db.create_budget_table()
        self.vendor_db = VendorDatabase("planpal.db")
        self.vendor_db.create_vendor_table()
        self.rundown_db = RundownDatabase("planpal.db")
        self.rundown_db.create_rundown_table()

        # Add sample data
        # self.add_sample_data()

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
                content=ft.Column(
                    controls=[
                        ft.ElevatedButton(text="Manage Events", on_click=self.open_manage_event),
                        ft.ElevatedButton(text="Go to Landing Page", on_click=self.open_landing_page)  # Add button to open landing page
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10
                ),
                alignment=ft.alignment.center
            )
        )

    def add_sample_data(self):
        # Check if there are any events in the database
        if not self.event_db.get_all_events():
            # Add sample events
            self.event_db.add_event(1, "Event A", "Location A", "2023-10-01", "Belum dimulai")
            self.event_db.add_event(2, "Event B", "Location B", "2023-10-02", "Sedang berlangsung")
            self.event_db.add_event(3, "Event C", "Location C", "2023-10-03", "Sudah selesai")

    def open_manage_event(self, e):
        # Clear the current page content
        self.page.controls.clear()
        # Initialize and display the EventManagerApp with the database instances
        EventManagerApp(self.page, self.event_db, self.guest_list_db, self.budget_db, self.vendor_db, self.rundown_db)
        self.page.update()

    def open_landing_page(self, e):
        # Clear the current page content
        self.page.controls.clear()
        # Initialize and display the LandingPage with the database instances
        LandingApp(self.page, self.event_db, self.guest_list_db, self.budget_db, self.vendor_db, self.rundown_db)
        self.page.update()

def main(page: ft.Page):
    app = PlanPal(page)

ft.app(target=main)