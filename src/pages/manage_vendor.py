import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import flet as ft
from src.database.controllervendor import ControllerVendor
from src.utils.buttons import *
from src.utils.pagesetup import PageSetup
from src.database.vendorForm import VendorForm

ITEMS_PER_PAGE = 5

class VendorManagerApp:
    def __init__(self, page):
        self.page = page
        self.page.title = "Vendor Management"

        # Setup page
        self.setup_page()

        self.controller = ControllerVendor()
        self.vendor_form = VendorForm()

        self.controller.add_vendor(1, "Vendor A", "0852", "baju")
        self.controller.add_vendor(2, "Vendor B", "idline", "lanyard")

        self.current_page = 0
        self.create_widgets()
        self.update_display()

    def setup_page(self):
        width = self.page.window.width
        height = self.page.window.height
        self.page.bgcolor = '#FFF5E9'

        # Set fonts
        self.page.fonts = {
            "Header": "C:/Users/Lenovo/Documents/RPL/tubes/PlanPal/src/assets/fonts/Fredoka/Fredoka-SemiBold.ttf",
            "Default_Bold": "C:/Users/Lenovo/Documents/RPL/tubes/PlanPal/src/assets/fonts/Afacad/Afacad-Bold.ttf",
            "Default_Regular": "C:/Users/Lenovo/Documents/RPL/tubes/PlanPal/src/assets/fonts/Afacad/Afacad-Regular.ttf",
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
                ft.DataColumn(ft.Text("Nama", color="#4539B4")),
                ft.DataColumn(ft.Text("Kontak Vendor", color="#4539B4")),
                ft.DataColumn(ft.Text("Produk/Jasa Vendor", color="#4539B4")),
                ft.DataColumn(ft.Text("")),
            ],
            rows=[],
            bgcolor="#FFF5E9",
            heading_row_color="#FAEBD9"
        )

        self.title = ft.Text(
            value="Vendor", 
            size=30, 
            weight=ft.FontWeight.BOLD, 
            color="#4539B4", 
            font_family="Default_Bold"
        )

        self.add_button = ft.ElevatedButton(
            text="Add Vendor",
            style=ft.ButtonStyle(
                padding=ft.padding.symmetric(horizontal=20, vertical=10),
                bgcolor="#C4E8F8",
                text_style=ft.TextStyle(
                    color="#4539B4",
                    weight=ft.FontWeight.BOLD,
                    font_family="Default_Bold",
                    size=20,
                )
            ),
            color="#4539B4", 
            on_click=self.add_vendor
        )

        self.back_button = BackButton(
        on_click_action=self.back_to_event_manager, font_family="Default_Bold"
        )

        self.prev_button = ft.ElevatedButton(text="Previous", on_click=self.prev_page, disabled=True)
        self.next_button = ft.ElevatedButton(text="Next", on_click=self.next_page, disabled=True)

        self.page.add(
            ft.Column(
                [   
                    ft.Container(
                        content=self.back_button,
                        alignment=ft.alignment.top_left,
                        padding=ft.padding.all(10),
                    ),
                    ft.Container(
                        content=self.title,
                        alignment=ft.alignment.center,
                        padding=ft.padding.only(bottom=10)
                    ),
                    ft.Container(
                        content=self.add_button,
                        alignment=ft.alignment.center,
                        padding=ft.padding.only(bottom=20)
                    ),
                    ft.Container(
                        content=self.tree,
                        alignment=ft.alignment.top_center,
                        expand=True
                    ),
                    ft.Row(
                        [self.prev_button, self.next_button],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                expand=True,
            )
        )

    def add_vendor(self, e):
        print("Add Vendor button clicked.")
        self.vendor_form.display_form(self.page, self.on_form_submit, is_edit=False)

    def back_to_event_manager(self, e):
        from src.pages.manage_event import EventManagerApp
        # Clear current page content
        self.page.controls.clear()
        # Load EventManagerApp
        EventManagerApp(self.page)
        self.page.update()

    def edit_vendor(self, event_id, vendor_name):
        print("Edit Vendor button clicked.")
        vendors = self.controller.get_vendor_by_event_id(event_id)

        print(f"Vendors retrieved for EventID {event_id}: {vendors}")
        vendor_data = next(
            (vendor for vendor in vendors if vendor["VendorName"] == vendor_name), None
        )

        if vendor_data:
            # Display a form populated with the vendor details for editing
            self.vendor_form.display_form(
                page=self.page,
                on_submit=self.on_form_submit,
                vendor_data=vendor_data,
                is_edit=True,
                original_event_id=event_id,
            )
            print(f"edit_vendor called with event_id={event_id}, vendor_name={vendor_name}")
        else:
            self.show_error_dialog(f"Vendor not found for Event ID '{event_id}'")

    def delete_vendor(self, event_id, vendor_name):
        if self.controller.get_vendor_by_event_id(event_id):
            self.controller.delete_vendor(event_id, vendor_name)
            self.update_display()
        else:
            self.show_error_dialog(f"Vendor not found for Event ID '{event_id}' and Vendor Name '{vendor_name}'.")

    def update_display(self):
        total_pages = (len(self.controller.get_vendor_by_event_id(1)) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

        self.prev_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page >= total_pages - 1

        start_index = self.current_page * ITEMS_PER_PAGE
        end_index = start_index + ITEMS_PER_PAGE

        total_vendors = self.controller.get_vendor_by_event_id(1)
        self.tree.rows.clear()  
        for vendor in total_vendors[start_index:end_index]:
            self.tree.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(vendor["VendorName"])),
                        ft.DataCell(ft.Text(vendor["VendorContact"])),
                        ft.DataCell(ft.Text(vendor["VendorProduct"])),
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    EditButton(
                                        on_click_action=lambda e, event_id=vendor["EventID"], vendor_name=vendor["VendorName"]: self.edit_vendor(event_id, vendor_name)
                                    ),
                                    DeleteButton(
                                        on_click_action=lambda e, event_id=vendor["EventID"], vendor_name=vendor["VendorName"]: self.delete_vendor(event_id, vendor_name)
                                    ),
                                ]
                            )
                        ),
                    ]
                )
            )

        self.page.update()

    def prev_page(self, e):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_display()

    def next_page(self, e):
        total_vendors = self.controller.get_vendor_by_event_id(1)
        total_pages = (len(total_vendors) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.update_display()

    def on_form_submit(self, form_data, is_edit, original_event_id):
        if is_edit:
            self.controller.edit_vendor(
                original_event_id, 
                form_data["VendorName"], 
                form_data["VendorContact"], 
                form_data["VendorProduct"]
                )
        else:
            self.controller.add_vendor(
                form_data["EventID"], 
                form_data["VendorName"], 
                form_data["VendorContact"], 
                form_data["VendorProduct"]
                )
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
    app = VendorManagerApp(page)

if __name__ == "__main__":
    ft.app(target=main)
