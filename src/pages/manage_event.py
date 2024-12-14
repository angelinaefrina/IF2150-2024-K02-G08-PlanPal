import sys
import os

# Add the src directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import flet as ft
from src.database.event import Event
from src.database.eventdisplay import EventDisplay
from src.database.formevent import FormEvent
from src.database.controllerevent import ControllerEvent
from src.utils.cards import EventCard
from src.utils.buttons import *
from src.utils.pagesetup import PageSetup

# Import Pages
from src.pages.manage_budget import BudgetManagerApp
from src.pages.manage_guest import GuestManagerApp
from src.pages.manage_vendor import VendorManagerApp
from src.pages.manage_rundown import RundownManagerApp

ITEMS_PER_PAGE = 6

class EventManagerApp:
    def __init__(self, page, event_db, guest_list_db, budget_db, vendor_db, rundown_db):
        self.page = page
        self.page.title = "PlanPal"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.event_db = event_db
        self.guest_list_db = guest_list_db
        self.budget_db = budget_db
        self.vendor_db = vendor_db
        self.rundown_db = rundown_db

        # Initialize dialog attribute
        self.dialog = None

        # Set up the page header first to ensure it is rendered on top
        self.setup_page()

        # Initialize ControllerEvent with EventDatabase
        self.controller = ControllerEvent(event_db)
        self.event_display = EventDisplay(self.controller.get_event_list())
        self.form_event = FormEvent()

        self.current_page = 0
        self.create_widgets()
        self.update_display()

    def setup_page(self):
        width = self.page.window.width
        height = self.page.window.height
        self.page.bgcolor = '#FFF5E9'

        # Set fonts
        self.page.fonts = {
            "Header": "../assets/fonts/Fredoka/Fredoka-SemiBold.ttf",
            "Default_Bold": "../assets/fonts/Afacad/Afacad-Bold.ttf",
            "Default_Regular": "../assets/fonts/Afacad/Afacad-Regular.ttf",
        }

        # Add the header (PlanPal text) at the top of the page
        self.page.add(
            ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Text("PlanPal", font_family="Header", color="#FFF5E9", size=64, weight=ft.FontWeight.BOLD),
                        width=width,
                        height=100,
                        bgcolor='#4539B4',
                        padding=ft.padding.all(5),
                        alignment=ft.alignment.top_left
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )

    def create_widgets(self):
        self.add_button = CreateNewEvent(on_click_action=self.add_event, font_family="Default_Bold")
        self.prev_button = ft.ElevatedButton(text="Previous", on_click=self.prev_page)
        self.next_button = ft.ElevatedButton(text="Next", on_click=self.next_page)

    def add_event(self, e):
        self.form_event.display_form(self.page, self.on_form_submit, is_edit=False)

    def edit_event(self, event_id):
        event_data = self.controller.get_event_details(event_id)
        if event_data:
            self.form_event.display_form(self.page, self.on_form_submit, event_data, is_edit=True, original_event_id=event_id)
        else:
            self.show_error_dialog(f"Event with ID '{event_id}' not found.")

    def delete_event(self, event_id):
        if self.controller.get_event_details(event_id):
            self.controller.delete_event(event_id)
            self.update_display()
        else:
            self.show_error_dialog(f"Event with ID '{event_id}' not found.")

    def view_event(self, page, event_id):
        event_data = self.controller.get_event_details(event_id)
        if event_data:
            self.dialog = ft.AlertDialog(
                title=ft.Text("Event Details"),
                content=ft.Column(
                    controls=[
                        ft.Text(f"Event ID: {event_data['EventID']}"),
                        ft.Text(f"Event Name: {event_data['EventName']}"),
                        ft.Text(f"Event Location: {event_data['EventLocation']}"),
                        ft.Text(f"Event Date: {event_data['EventDate']}"),
                        ft.Text(f"Event Status: {event_data['EventStatus']}")
                    ],
                        height=300,
                    spacing=20,
                    alignment=ft.MainAxisAlignment.START
                ),
                actions=[ft.TextButton("Lihat Anggaran", on_click=self.open_budget_page),
                         ft.TextButton("Lihat Rundown", on_click=self.open_rundown_page),
                         ft.TextButton("Daftar Vendor", on_click=lambda e: self.open_vendor_page(e, event_id, self.event_db, self.guest_list_db, self.budget_db, self.vendor_db, self.rundown_db)),
                         ft.TextButton("Daftar Tamu", on_click=lambda e: self.open_guest_page(e, event_id, self.event_db, self.guest_list_db, self.budget_db, self.vendor_db, self.rundown_db)),
                        ]
            )
            page.dialog = self.dialog
            self.dialog.open = True
            page.update()

        else:
            self.show_error_dialog(f"Event with ID '{event_id}' not found.")

    def update_display(self):
        # Refresh the event list from the database
        self.event_display.event_list = self.controller.get_event_list()
        total_pages = len(self.event_display.event_list) // ITEMS_PER_PAGE + (1 if len(self.event_display.event_list) % ITEMS_PER_PAGE > 0 else 0)

        # Remove dynamic controls (event cards, etc.) if needed
        dynamic_controls = self.page.controls[1:]  # Assuming the header is the first control
        for control in dynamic_controls:
            self.page.controls.remove(control)

        start_index = self.current_page * ITEMS_PER_PAGE
        end_index = start_index + ITEMS_PER_PAGE
        events_to_display = self.event_display.event_list[start_index:end_index]

        rows = []
        row = []
        for index, event in enumerate(events_to_display):
            card = EventCard(
                event_title=event[1],
                event_date=event[3],
                on_view_details_click=lambda e, event_id=event[0]: self.view_event(self.page, event_id),
                on_edit_click=lambda e, event_id=event[0]: self.edit_event(event_id),
                on_delete_click=lambda e, event_id=event[0]: self.delete_event(event_id)
            )
            row.append(card)
            if len(row) == 3 or index == len(events_to_display) - 1:
                rows.append(ft.Row(controls=row, spacing=20, alignment=ft.MainAxisAlignment.CENTER))
                row = []

        display_container = ft.Container(
            content=ft.Column(
                controls=rows,
                spacing=20,
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
            expand=True,
            alignment=ft.alignment.top_center,
        )

        self.prev_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page >= total_pages - 1

        self.page.add(
            ft.Column(
                [   
                    ft.Text("All Events", font_family="Default_Bold", size=24, color="#4539B4"),
                    ft.Column(
                    controls=rows,
                    spacing=20,
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
                    ),
                    ft.Row(
                        [
                            self.prev_button,
                            self.next_button,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20,
                    ),
                    ft.Container(
                    content=self.add_button,
                    alignment=ft.alignment.center,
                    ),
                ],
                alignment=ft.MainAxisAlignment.END,
                expand=True,
            )
        )
        self.page.update()

    def prev_page(self, e):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_display()

    def next_page(self, e):
        total_pages = len(self.event_display.event_list) // ITEMS_PER_PAGE + (1 if len(self.event_display.event_list) % ITEMS_PER_PAGE > 0 else 0)
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.update_display()

    def on_form_submit(self, form_data, is_edit, original_event_id=None):
        if form_data:
            if is_edit:
                self.controller.delete_event(original_event_id)
                self.controller.add_event(
                    original_event_id,
                    form_data["EventName"],
                    form_data["EventLocation"],
                    form_data["EventDate"],
                    form_data["EventStatus"]
                )
                self.show_success_dialog("Event updated successfully!")
            else:
                new_event_id = self.event_db.get_max_event_id() + 1
                self.controller.add_event(
                    new_event_id,
                    form_data["EventName"],
                    form_data["EventLocation"],
                    form_data["EventDate"],
                    form_data["EventStatus"]
                )
                self.show_success_dialog("Event added successfully!")
            self.update_display()

    def show_error_dialog(self, message):
        self.dialog = ft.AlertDialog(
            title=ft.Text("Error"),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=lambda e: self.close_error_dialog())]
        )
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()

    def show_success_dialog(self, message):
        self.dialog = ft.AlertDialog(
            title=ft.Text("Success"),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=lambda e: self.close_success_dialog())]
        )
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()

    def close_error_dialog(self):
        if self.dialog:
            self.dialog.open = False
            self.page.update()

    def close_success_dialog(self):
        if self.dialog:
            self.dialog.open = False
            self.page.update()

    def open_budget_page(self, e):
        self.page.controls.clear()
        if self.dialog:
            self.dialog.open = False
        BudgetManagerApp(self.page)
        self.page.update()

    def open_guest_page(self, e, event_id, event_db, guest_list_db, budget_db, vendor_db, rundown_db):
        self.page.controls.clear()
        if self.dialog:
            self.dialog.open = False
        GuestManagerApp(self.page, event_id, event_db, guest_list_db, budget_db, vendor_db, rundown_db)
        self.page.update()

    def open_vendor_page(self, e, event_id, event_db, guest_list_db, budget_db, vendor_db, rundown_db):
        self.page.controls.clear()
        if self.dialog:
            self.dialog.open = False
        VendorManagerApp(self.page, event_id, event_db, guest_list_db, budget_db, vendor_db, rundown_db)
        self.page.update()

    def open_rundown_page(self, e):
        self.page.controls.clear()
        if self.dialog:
            self.dialog.open = False
        RundownManagerApp(self.page)
        self.page.update()

def main(page: ft.Page):
    app = EventManagerApp(page, event_db, guest_list_db, budget_db, vendor_db, rundown_db)

if __name__ == "__main__":
    ft.app(target=main)