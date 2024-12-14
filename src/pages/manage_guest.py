import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import flet as ft
from src.database.guestcontroller import GuestController
from src.database.guestlistform import GuestListForm
from src.utils.buttons import *
from src.utils.pagesetup import PageSetup

ITEMS_PER_PAGE = 5
class GuestManagerApp:
    def __init__(self, page, event_id, event_db, guest_list_db, budget_db, vendor_db, rundown_db):
        self.page = page
        self.page.title = "Guest Management"
        self.event_id = event_id

        # Setup page
        self.setup_page()

        self.controller = GuestController()
        self.guest_list_form = GuestListForm()
        self.event_db = event_db
        self.guest_list_db = guest_list_db
        self.budget_db = budget_db
        self.vendor_db = vendor_db
        self.rundown_db = rundown_db

        self.controller.add_guest_list(1, "Alice", "Hadir")
        self.controller.add_guest_list(1, "Bob", "Menyusul")
        self.controller.add_guest_list(1, "Charlie", "Tidak Hadir")
        self.controller.display_guest_list(event_id)

        # Pagination variables
        self.current_page = 0
        self.create_widgets()
        self.update_display()

    def setup_page(self):
        width = self.page.window.width
        height = self.page.window.height
        self.page.bgcolor = '#FFF5E9'

        # Set fonts
        self.page.fonts = {
            "Header": "./src/assets/fonts/Fredoka/Fredoka-SemiBold.ttf",
            "Default_Bold": "./src/assets/fonts/Afacad/Afacad-Bold.ttf",
            "Default_Regular": "./src/assets/fonts/Afacad/Afacad-Regular.ttf",
        }
        # Header PlanPal
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
        self.tree = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nama Tamu", color="#4539B4")),
                ft.DataColumn(ft.Text("Status RSVP", color="#4539B4")),
                ft.DataColumn(ft.Text(" ")),
            ],
            rows=[],
            bgcolor="#FFF5E9",
            heading_row_color="#FAEBD9"
        )

        self.title = ft.Text(
            value= "Daftar Tamu", 
            size=30, 
            weight=ft.FontWeight.BOLD, 
            color="#4539B4",
            font_family="Default_Bold"
            )
        
        self.add_button = ft.ElevatedButton(
            text="Add Guest",
            style=ft.ButtonStyle(
                padding=ft.padding.symmetric(horizontal=20, vertical=10),
                bgcolor= "#C4E8F8",
                text_style= ft.TextStyle(
                    color= "#4539B4",
                    weight= ft.FontWeight.BOLD,
                    font_family="Default_Bold",
                    size=20,
                )
            ),
            color="#4539B4",
            on_click=lambda e: self.add_guest(e, self.event_id, guest_id=None)
        )

        self.back_button = BackButton(
        on_click_action=self.back_to_event_manager, font_family="Default_Bold"
        )

        self.prev_button = ft.ElevatedButton("Previous", on_click=self.prev_page, disabled=True)
        self.next_button = ft.ElevatedButton("Next", on_click=self.next_page, disabled=True)
        
        self.page.add(
            ft.Column(
                [   
                    ft.Container(
                        content=self.back_button,
                        alignment=ft.alignment.top_left,
                        padding=ft.padding.all(10),
                    ),
                    ft.Container(
                        content= self.title,
                        alignment= ft.alignment.center,
                        padding= ft.padding.only(bottom=10)
                    ),
                    ft.Container(
                        content= self.add_button,
                        alignment= ft.alignment.center,
                        padding= ft.padding.only(bottom=20)
                    ),
                    ft.Container(
                        content= self.tree,
                        alignment= ft.alignment.top_center,
                        expand= True
                    ),
                    ft.Row(
                        [self.prev_button, self.next_button],
                        alignment= ft.MainAxisAlignment.CENTER,
                        spacing= 20,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                expand=True,
            )
        )

    def add_guest(self, e, event_id, guest_id):
        self.guest_list_form.display_form(self.page, self.on_form_submit, event_id, guest_id, is_edit=False)

    def back_to_event_manager(self, e):
        from src.pages.manage_event import EventManagerApp
        # Clear current page content
        self.page.controls.clear()
        # Load EventManagerApp
        EventManagerApp(self.page, self.event_db, self.guest_list_db, self.budget_db, self.vendor_db, self.rundown_db)
        self.page.update()
        
    def edit_guest(self, event_id, guest_id):
        print(f"Editing budget for EventID: {event_id}")
        guest_list = self.controller.get_guest_list(event_id)
        
        guest_data = next(
            (guest for guest in guest_list if guest["GuestID"] == guest_id), None
        )

        if guest_data:
            self.guest_list_form.display_form(
                page=self.page, 
                on_submit=self.on_form_submit,
                event_id=event_id,
                guest_id=guest_id, 
                guest_list_data=guest_data, 
                is_edit=True, 
            )
            print(f"edit_vendor called with event_id={event_id}, guest_id={guest_id}")
        else:
            self.show_error_dialog("Guest not found.")
    
    def delete_guest(self, event_id, guest_id):
        if self.controller.get_guest_list(event_id):
            self.controller.delete_guest_list(event_id, guest_id)
            self.update_display()
        else:
            self.show_error_dialog("Guest not found.")

    def update_display(self):
        total_pages = (len(self.controller.get_guest_list(self.event_id)) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

        self.prev_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page >= total_pages - 1

        start_index = self.current_page * ITEMS_PER_PAGE
        end_index = start_index + ITEMS_PER_PAGE

        guests_to_display = self.controller.get_guest_list(self.event_id)
        self.tree.rows.clear()
        for guest in guests_to_display[start_index:end_index]:
            self.tree.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(guest["GuestName"], color="#4539B4")),
                        ft.DataCell(ft.Text(guest["RSVPStatus"], color="#4539B4")),
                        ft.DataCell(
                            ft.Row(
                                controls=
                                    [
                                        EditButton(on_click_action=lambda e, event_id=guest["EventID"], guest_id=guest["GuestID"]: self.edit_guest(event_id, guest_id)),
                                        DeleteButton(on_click_action=lambda e, event_id=guest["EventID"], guest_id=guest["GuestID"]: self.delete_guest(event_id, guest_id)),
                                    ]
                            )
                        ),
                    ]
                )
            )
        self.page.update()

    def on_form_submit(self, form_data, is_edit, event_id, guest_id):
        if is_edit:
            self.controller.edit_guest_list(
                event_id,
                guest_id, 
                form_data["GuestName"],
                form_data["RSVPStatus"]
                )
        else:
            self.controller.add_guest_list(
                event_id,
                form_data["GuestName"], 
                form_data["RSVPStatus"]
                )
        self.update_display()

    def prev_page(self, e):
        """Go to the previous page."""
        if self.current_page > 1:
            self.current_page -= 1
            self.update_display()
            self.page.update()

    def next_page(self, e):
        """Go to the next page."""
        total_guests = self.controller.get_guest_list(self.event_id)
        total_pages = (len(total_guests) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
        if self.current_page < total_pages:
            self.current_page += 1
            self.update_display()
            self.page.update()

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


    
# def main(page: ft.Page):
#     app = GuestManagerApp(page, 1)

# if __name__ == "__main__":
#     ft.app(target=main)