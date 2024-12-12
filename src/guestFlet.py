import flet as ft
from guestcontroller import GuestController

class GuestManagerApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "PlanPal Guest Manager"
        self.page.bgcolor = "#FFF5E9"
        
        self.guest_controller = GuestController()
        self.guest_list_container = ft.Container()

        # Pagination variables
        self.current_page = 1
        self.guests_per_page = 8

        # Input components
        self.guest_name_input = ft.TextField(label="Nama Tamu", autofocus=True)
        self.rsvp_status_input = ft.Dropdown(
            label="Status RSVP",
            options=[
                ft.dropdown.Option("Hadir"),
                ft.dropdown.Option("Tidak Hadir"),
                ft.dropdown.Option("Menyusul"),
            ],
        )

        # UI components
        self.previous_button = ft.ElevatedButton("Previous", on_click=self.previous_page)
        self.next_button = ft.ElevatedButton("Next", on_click=self.next_page)
        self.guest_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nama Tamu", color="#4539B4", size=20)),
                ft.DataColumn(ft.Text("Status RSVP", color="#4539B4", size=20)),
                ft.DataColumn(ft.Text(" ")),
            ],
            rows=[],
        )

        self.build_ui()
        self.update_ui()

    def build_ui(self):
        """Build the main UI."""
        self.page.add(
            ft.Column(
                [
                    # Header
                    ft.Container(
                        content=ft.Text(
                            "PlanPal", size=40, weight=ft.FontWeight.BOLD, color="#FFF5E9"
                        ),
                        bgcolor="#4539B4",
                        padding=ft.padding.symmetric(horizontal=16, vertical=6),
                        alignment=ft.alignment.center_left,
                        expand=True,
                    ),
                    # Title
                    ft.Row(
                        [ft.Text("Daftar Tamu", size=30, weight=ft.FontWeight.BOLD, color="#4539B4")],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    # Add Button
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                content=ft.Text("Tambah", weight=ft.FontWeight.BOLD, color="#4539B4"),
                                on_click=self.add_guest,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Divider(),
                    # Guest List Container
                    self.guest_list_container,
                    # Pagination
                    ft.Row(
                        [
                            self.previous_button,
                            ft.Text(f"Page {self.current_page} of {len(self.guest_controller.guest_list) // self.guests_per_page + 1}", size=12),
                            self.next_button,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ]
            )
        )

    def update_ui(self):
        """Update guest list UI."""
        self.update_guest_list()
        self.page.update()

    def update_guest_list(self):
        """Update the guest list table with pagination."""
        start_index = (self.current_page - 1) * self.guests_per_page
        end_index = start_index + self.guests_per_page
        guests_to_display = self.guest_controller.guest_list[start_index:end_index]

        self.guest_table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(guest["GuestName"], color="#4539B4")),
                    ft.DataCell(ft.Text(guest["RSVPStatus"], color="#4539B4")),
                    ft.DataCell(
                        ft.Row(
                            [
                                ft.IconButton(
                                    icon=ft.icons.EDIT,
                                    on_click=lambda e, idx=index: self.edit_guest(idx),
                                ),
                                ft.IconButton(
                                    icon=ft.icons.DELETE,
                                    icon_color=ft.colors.RED,
                                    on_click=lambda e, idx=index: self.delete_guest(idx),
                                ),
                            ]
                        )
                    ),
                ]
            )
            for index, guest in enumerate(guests_to_display)
        ]
        self.guest_list_container.content = self.guest_table
        self.page.update()

    def previous_page(self, e):
        """Go to the previous page."""
        if self.current_page > 1:
            self.current_page -= 1
            self.update_guest_list()
            self.page.update()

    def next_page(self, e):
        """Go to the next page."""
        total_pages = len(self.guest_controller.guest_list) // self.guests_per_page + 1
        if self.current_page < total_pages:
            self.current_page += 1
            self.update_guest_list()
            self.page.update()

    def add_guest(self, e):
        """Show dialog to add a new guest."""
        self.show_add_guest_dialog()

    def show_add_guest_dialog(self):
        """Display the Add Guest dialog."""
        self.guest_name_input.value = ""
        self.rsvp_status_input.value = None

        add_guest_dialog = ft.AlertDialog(
            title=ft.Text("Tambah Tamu", color="#4539B4"),
            content=ft.Column([self.guest_name_input, self.rsvp_status_input]),
            actions=[
                ft.TextButton("Keluar", on_click=lambda _: self.close_dialog(add_guest_dialog)),
                ft.TextButton("Tambah", on_click=lambda _: self.validate_add_guest(add_guest_dialog)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor="#FFF5E9",
        )
        self.page.dialog = add_guest_dialog
        add_guest_dialog.open = True
        self.page.update()

    def validate_add_guest(self, dialog):
        """Validate input before adding a new guest."""
        guest_name = self.guest_name_input.value.strip()
        rsvp_status = self.rsvp_status_input.value

        if not guest_name or not rsvp_status:
            return  # Display validation errors
        self.save_new_guest(dialog)

    def save_new_guest(self, dialog):
        """Save a new guest."""
        guest_name = self.guest_name_input.value.strip()
        rsvp_status = self.rsvp_status_input.value
        self.guest_controller.add_guest_list(guest_name, rsvp_status)
        self.close_dialog(dialog)
        self.update_ui()

    def edit_guest(self, index):
        """Edit a guest."""
        guest = self.guest_controller.guest_list[index]
        self.show_edit_guest_dialog(index, guest["GuestName"], guest["RSVPStatus"])

    def show_edit_guest_dialog(self, index, guest_name, rsvp_status):
        """Show the Edit Guest dialog."""
        self.guest_name_input.value = guest_name
        self.rsvp_status_input.value = rsvp_status

        edit_guest_dialog = ft.AlertDialog(
            title=ft.Text("Edit Tamu", color="#4539B4"),
            content=ft.Column([self.guest_name_input, self.rsvp_status_input]),
            actions=[
                ft.TextButton("Keluar", on_click=lambda _: self.close_dialog(edit_guest_dialog)),
                ft.TextButton("Simpan", on_click=lambda _: self.save_edited_guest(index, edit_guest_dialog)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor="#FFF5E9",
        )
        self.page.dialog = edit_guest_dialog
        edit_guest_dialog.open = True
        self.page.update()

    def save_edited_guest(self, index, dialog):
        """Save the edited guest."""
        guest_name = self.guest_name_input.value.strip()
        rsvp_status = self.rsvp_status_input.value
        self.guest_controller.edit_guest_list(self.guest_controller.guest_list[index]["GuestID"], guest_name, rsvp_status)
        self.close_dialog(dialog)
        self.update_ui()

    def delete_guest(self, index):
        """Delete a guest."""
        guest = self.guest_controller.guest_list[index]
        self.show_confirmation_dialog(
            title="Hapus Tamu",
            content=f"Yakin ingin menghapus tamu '{guest['GuestName']}'?",
            on_confirm=lambda: self.confirm_delete_guest(index),
        )

    def confirm_delete_guest(self, index):
        """Confirm deletion of a guest."""
        self.guest_controller.delete_guest_list(self.guest_controller.guest_list[index]["GuestID"])
        self.update_ui()

    def show_confirmation_dialog(self, title, content, on_confirm):
        """Display a confirmation dialog."""
        confirmation_dialog = ft.AlertDialog(
            title=ft.Text(title, color="#4539B4"),
            content=ft.Text(content, color="#4539B4"),
            actions=[
                ft.TextButton("Tidak", on_click=lambda _: self.close_dialog(confirmation_dialog)),
                ft.TextButton("Ya", on_click=lambda _: (self.close_dialog(confirmation_dialog), on_confirm())),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor="#FFF5E9",
        )
        self.page.dialog = confirmation_dialog
        confirmation_dialog.open = True
        self.page.update()

    def close_dialog(self, dialog):
        """Close a dialog."""
        dialog.open = False
        self.page.update()

def main(page: ft.Page):
    app = GuestManagerApp(page)

if __name__ == "__main__":
    ft.app(target=main)
