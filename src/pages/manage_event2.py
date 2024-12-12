import sys
import os

# YANG ADA SORT EVENT NYA DI FILE INI YAA HEHE AKU TAKUT CONFLICT KALO DI MANAGE_EVENT.PY SORRYYYY

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

ITEMS_PER_PAGE = 6

class EventManagerApp:
    def __init__(self, page):
        self.page = page
        self.page.title = "Event Manager"

        # Set up the page header first to ensure it is rendered on top
        self.setup_page()

        # Now add EventManagerApp components
        self.controller = ControllerEvent()
        self.event_display = EventDisplay(self.controller.get_event_list())
        self.form_event = FormEvent()

        # Sample event data
        self.controller.add_event(1, "Event A", "Location A", "2023-10-01", "Belum dimulai")
        self.controller.add_event(2, "Event B", "Location B", "2023-10-02", "Sedang berlangsung")
        self.controller.add_event(3, "Event C", "Location C", "2023-10-03", "Sudah selesai")
        self.event_display.event_list = self.controller.get_event_list()

        self.current_page = 0
        self.create_widgets()
        self.update_display()

    def setup_page(self):
        width = self.page.window.width
        height = self.page.window.height
        self.page.bgcolor = '#FFF5E9'

        # Set fonts
        self.page.fonts = {
            "Header": "C:/Users/Anella Utari/Documents/GitHub/IF2150-2024-K02-G08-PlanPal/src/assets/fonts/Fredoka/Fredoka-SemiBold.ttf",
            "Default_Bold": "C:/Users/Anella Utari/Documents/GitHub/IF2150-2024-K02-G08-PlanPal/src/assets/fonts/Afacad/Afacad-Bold.ttf",
            "Default_Regular": "C:/Users/Anella Utari/Documents/GitHub/IF2150-2024-K02-G08-PlanPal/src/assets/fonts/Afacad/Afacad-Regular.ttf",
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
        self.add_button = CreateNewEvent(on_click_action=self.add_event)
        self.prev_button = ft.ElevatedButton(text="Previous", on_click=self.prev_page)
        self.next_button = ft.ElevatedButton(text="Next", on_click=self.next_page)

        self.sort_dropdown = ft.Dropdown(
            label="Sort by Status",
            width=200,
            options=[
                ft.dropdown.Option("Semua"),
                ft.dropdown.Option("Belum dimulai"),
                ft.dropdown.Option("Sedang berlangsung"),
                ft.dropdown.Option("Sudah selesai"),
                ft.dropdown.Option("Dibatalkan"),
            ],
            on_change=self.sort_events_by_status
        )

        self.dropdown_container = ft.Container(
            content=ft.Row(
                controls=[self.sort_dropdown],
                alignment=ft.MainAxisAlignment.END,
            ),
            padding=ft.padding.only(right=20,top=10),
        )
    
    def sort_events_by_status(self,e):
        selected_status = e.control.value
        self.clear_dynamic_controls()
        
        if selected_status == "Semua":
            self.event_display.event_list = self.controller.get_event_list()
            self.update_display()
        else:
            filtered_events = [event for event in self.controller.get_event_list() if event["EventStatus"] == selected_status]
    
            if not filtered_events:
                no_events_message = ft.Container(
                    content=ft.Text(
                        f"Tidak ada event dengan status '{selected_status}'.",
                        size=24,
                        color="#4539B4", 
                        font_family="Default_Bold",
                    ),
                    alignment=ft.alignment.center,
                    expand=True
                )
                self.page.add(
                    ft.Column(
                        controls=[
                            self.dropdown_container,
                            no_events_message,
                            ft.Container(
                                content=self.add_button,
                                alignment=ft.alignment.center,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        expand=True,
                    )
                )
                self.page.update()
            else:
                self.event_display.event_list = filtered_events
                self.update_display()

    def clear_dynamic_controls(self):
        dynamic_controls = self.page.controls[1:]
        for control in dynamic_controls:
            self.page.controls.remove(control)
        self.page.update()

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

    def view_event(self, event_id):
        event_data = self.controller.get_event_details(event_id)
        if event_data:
            self.form_event.display_form(self.page, self.on_form_submit, event_data, is_edit=False, original_event_id=event_id)
        else:
            self.show_error_dialog(f"Event with ID '{event_id}' not found.")

    def update_display(self):
        total_pages = len(self.event_display.event_list) // ITEMS_PER_PAGE + (1 if len(self.event_display.event_list) % ITEMS_PER_PAGE > 0 else 0)

        self.clear_dynamic_controls()

        start_index = self.current_page * ITEMS_PER_PAGE
        end_index = start_index + ITEMS_PER_PAGE
        events_to_display = self.event_display.event_list[start_index:end_index]

        rows = []
        row = []
        for index, event in enumerate(events_to_display):
            card = EventCard(
                event_title=event["EventName"],
                event_date=event["EventDate"],
                on_view_details_click=lambda e, event_id=event["EventID"]: self.view_event(event_id),
                on_edit_click=lambda e, event_id=event["EventID"]: self.edit_event(event_id),
                on_delete_click=lambda e, event_id=event["EventID"]: self.delete_event(event_id)
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

        # self.page.add(display_container)

        self.prev_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page >= total_pages - 1

        self.page.add(
            ft.Column(
                controls=[   
                    self.dropdown_container,
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
                # Check if the new EventID already exists
                if original_event_id != form_data["EventID"] and self.controller.get_event_details(form_data["EventID"]):
                    self.show_error_dialog(f"Event with ID '{form_data['EventID']}' already exists.")
                else:
                    self.controller.delete_event(original_event_id)
                    self.controller.add_event(
                        form_data["EventID"],
                        form_data["EventName"],
                        form_data["EventLocation"],
                        form_data["EventDate"],
                        form_data["EventStatus"]
                    )
                    self.show_success_dialog("Event updated successfully!")
            else:
                if original_event_id != form_data["EventID"] and self.controller.get_event_details(form_data["EventID"]):
                    self.show_error_dialog(f"Event with ID '{form_data['EventID']}' already exists.")
                else:
                    self.controller.add_event(
                        form_data["EventID"],
                        form_data["EventName"],
                        form_data["EventLocation"],
                        form_data["EventDate"],
                        form_data["EventStatus"]
                    )
                    self.show_success_dialog("Event added successfully!")
            self.update_display()

    def show_error_dialog(self, message):
        error_dialog = ft.AlertDialog(
            title=ft.Text("Error"),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=lambda e: self.close_error_dialog())]
        )
        self.page.dialog = error_dialog
        error_dialog.open = True
        self.page.update()

    def show_success_dialog(self, message):
        success_dialog = ft.AlertDialog(
            title=ft.Text("Success"),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=lambda e: self.close_success_dialog())]
        )
        self.page.dialog = success_dialog
        success_dialog.open = True
        self.page.update()

    def close_error_dialog(self):
        self.page.dialog.open = False
        self.page.update()

    def close_success_dialog(self):
        self.page.dialog.open = False
        self.page.update()

def main(page: ft.Page):
    app = EventManagerApp(page)

if __name__ == "__main__":
    ft.app(target=main)
