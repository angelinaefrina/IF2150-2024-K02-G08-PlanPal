import flet as ft
from guestcontroller import GuestController

current_page = 1
guests_per_page = 8

def main(page: ft.Page):
    guest_controller = GuestController()
    guest_list_container = ft.Container()

    page.bgcolor = "#FFF5E9"

    # Define table columns
    guest_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nama Tamu", color="#4539B4", size=20)),
            ft.DataColumn(ft.Text("Status RSVP", color="#4539B4", size=20)),
            ft.DataColumn(ft.Text(" ")),
        ],
        rows=[],
    )

    def update_guest_list():
        """Update the guest list table with pagination."""
        start_index = (current_page - 1) * guests_per_page
        end_index = start_index + guests_per_page
        guests_to_display = guest_controller.guest_list[start_index:end_index]

        guest_table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(guest["GuestName"], color="#4539B4")),
                    ft.DataCell(ft.Text(guest["RSVPStatus"], color="#4539B4")),
                    ft.DataCell(
                        ft.Row(
                            [
                                ft.IconButton(
                                    icon=ft.icons.EDIT,
                                    on_click=lambda e, idx=index: edit_guest(idx),
                                ),
                                ft.IconButton(
                                    icon=ft.icons.DELETE,
                                    on_click=lambda e, idx=index: delete_guest(idx),
                                ),
                            ]
                        )
                    ),
                ]
            )
            for index, guest in enumerate(guests_to_display)
        ]
        guest_list_container.content = guest_table
        page.update()

    def previous_page(e):
        """Go to the previous page."""
        global current_page
        if current_page > 1:
            current_page -= 1
            update_guest_list()
            update_pagination_buttons()
            page.update()

    def next_page(e):
        """Go to the next page."""
        global current_page
        if current_page < guests_per_page < len(guest_controller.guest_list) :
            current_page += 1
            update_guest_list()
            update_pagination_buttons()
            page.update()

    def update_pagination_buttons():
        """Update the pagination buttons."""
        global current_page
        pagination_text = f"Page {current_page} of {len(guest_controller.guest_list) // guests_per_page + 1}"
        page.controls[1].text = pagination_text  # Update the pagination text control
        page.update()  # Ensure the page is updated with the new text

    previous_button = ft.ElevatedButton("Previous", on_click=previous_page)
    next_button = ft.ElevatedButton("Next", on_click=next_page)

    def update_ui():
        """Update guest list UI."""
        update_guest_list()
        page.update()

    def add_guest(e):
        """Show dialog to add a new guest."""
        show_add_guest_dialog()

    def show_add_guest_dialog():
        """Display the Add Guest dialog."""
        guest_name_input.value = ""
        rsvp_status_input.value = None

        # Reset the input fields to default state (no errors)
        guest_name_input.border_color = ft.colors.BLACK
        guest_name_input.helper_text = ""
        guest_name_input.helper_text_color = ft.colors.TRANSPARENT
        
        rsvp_status_input.border_color = ft.colors.BLACK
        rsvp_status_input.helper_text = ""
        rsvp_status_input.helper_text_color = ft.colors.TRANSPARENT

        add_guest_dialog = ft.AlertDialog(
            title=ft.Text("Tambah Tamu", color="#4539B4"),
            content=ft.Column([guest_name_input, rsvp_status_input]),
            actions=[
                ft.TextButton("Keluar", on_click=lambda _: close_dialog(add_guest_dialog)),
                ft.TextButton("Tambah", on_click=lambda _: validate_add_guest(add_guest_dialog)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor="#FFF5E9",
        )
        page.dialog = add_guest_dialog
        add_guest_dialog.open = True
        page.update()
    
    def validate_add_guest(dialog):
        """Validate input before adding a new guest."""
        guest_name = guest_name_input.value.strip()
        rsvp_status = rsvp_status_input.value

        # Validasi jika input kosong dan ubah warna border menjadi merah
        if not guest_name or not rsvp_status:
            # Ubah border color menjadi merah jika input kosong
            guest_name_input.border_color = ft.colors.RED
            guest_name_input.helper_text = "This field is required!"
            guest_name_input.helper_text_color = ft.colors.RED
            if not rsvp_status:
                rsvp_status_input.border_color = ft.colors.RED
                rsvp_status_input.helper_text = "This field is required!"
                rsvp_status_input.helper_text_color = ft.colors.RED

            page.update()
            return

        # Proceed with confirmation dialog
        show_confirmation_dialog(
            title="Tambah Tamu",
            content=f"Yakin ingin menambahkan tamu '{guest_name}'?",
            on_confirm=lambda: save_new_guest(dialog),
            bgcolor="#FFF5E9"
        )

    def save_new_guest(dialog):
        """Save a new guest."""
        guest_name = guest_name_input.value.strip()
        rsvp_status = rsvp_status_input.value
        guest_controller.add_guest_list(guest_name, rsvp_status)
        
        # Reset form inputs
        guest_name_input.border_color = ft.colors.BLACK
        guest_name_input.helper_text = ""
        guest_name_input.helper_text_color = ft.colors.TRANSPARENT
        
        rsvp_status_input.border_color = ft.colors.BLACK
        rsvp_status_input.helper_text = ""
        rsvp_status_input.helper_text_color = ft.colors.TRANSPARENT

        close_dialog(dialog)
        update_ui()

    def edit_guest(index):
        """Show dialog to edit a guest."""
        guest = guest_controller.guest_list[index]
        show_edit_guest_dialog(index, guest["GuestName"], guest["RSVPStatus"])

    def show_edit_guest_dialog(index, guest_name, rsvp_status):
        """Display the Edit Guest dialog."""
        guest_name_input.value = guest_name
        rsvp_status_input.value = rsvp_status

        # Reset the input fields to default state (no errors)
        guest_name_input.border_color = ft.colors.BLACK
        guest_name_input.helper_text = ""
        guest_name_input.helper_text_color = ft.colors.TRANSPARENT
        
        rsvp_status_input.border_color = ft.colors.BLACK
        rsvp_status_input.helper_text = ""
        rsvp_status_input.helper_text_color = ft.colors.TRANSPARENT

        edit_guest_dialog = ft.AlertDialog(
            title=ft.Text("Edit Tamu"),
            content=ft.Column([guest_name_input, rsvp_status_input]),
            actions=[
                ft.TextButton("Keluar", on_click=lambda _: close_dialog(edit_guest_dialog)),
                ft.TextButton("Simpan", on_click=lambda _: validate_edit_guest(index, edit_guest_dialog)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor="#FFF5E9",
        )
        page.dialog = edit_guest_dialog
        edit_guest_dialog.open = True
        page.update()
    
    def validate_edit_guest(index, dialog):
        """Validate input before editing a guest."""
        guest_name = guest_name_input.value.strip()
        rsvp_status = rsvp_status_input.value

        # Validasi jika input kosong dan ubah warna border menjadi merah
        if not guest_name or not rsvp_status:
            # Ubah border color menjadi merah jika input kosong
            guest_name_input.border_color = ft.colors.RED
            guest_name_input.helper_text = "This field is required!"
            guest_name_input.helper_text_color = ft.colors.RED
            if not rsvp_status:
                rsvp_status_input.border_color = ft.colors.RED
                rsvp_status_input.helper_text = "This field is required!"
                rsvp_status_input.helper_text_color = ft.colors.RED

            page.update()
            return

        # Proceed with confirmation dialog
        show_confirmation_dialog(
            title="Edit Tamu",
            content=f"Yakin ingin menyimpan perubahan tamu '{guest_name}'?",
            on_confirm=lambda: save_edited_guest(index, dialog),
            bgcolor="#FFF5E9",
        )

    def save_edited_guest(index, dialog):
        """Save the edited guest."""
        guest_name = guest_name_input.value.strip()
        rsvp_status = rsvp_status_input.value
        guest_controller.edit_guest_list(guest_controller.guest_list[index]["GuestID"], guest_name, rsvp_status)
        
        # Reset form inputs
        guest_name_input.border_color = ft.colors.BLACK
        guest_name_input.helper_text = ""
        guest_name_input.helper_text_color = ft.colors.TRANSPARENT
        
        rsvp_status_input.border_color = ft.colors.BLACK
        rsvp_status_input.helper_text = ""
        rsvp_status_input.helper_text_color = ft.colors.TRANSPARENT
        
        close_dialog(dialog)
        update_ui()

    def delete_guest(index):
        """Delete a guest."""
        guest = guest_controller.guest_list[index]
        show_confirmation_dialog(
            title="Hapus Tamu",
            content=f"Yakin ingin menghapus tamu '{guest['GuestName']}'?",
            on_confirm=lambda: confirm_delete_guest(index),
            bgcolor="#FFF5E9",
        )
    
    def confirm_delete_guest(index):
        """Confirm deletion of a guest."""
        guest_controller.delete_guest_list(guest_controller.guest_list[index]["GuestID"])
        update_ui()

    def show_confirmation_dialog(title, content, on_confirm,bgcolor):
        """Display a confirmation dialog."""
        confirmation_dialog = ft.AlertDialog(
            title=ft.Text(title, color="#4539B4"),
            content=ft.Text(content, color="#4539B4"),
            actions=[
                ft.TextButton("Tidak", on_click=lambda _: close_dialog(confirmation_dialog)),
                ft.TextButton("Ya", on_click=lambda _: (
                    close_dialog(confirmation_dialog),
                    on_confirm(),
                )),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=bgcolor,
        )
        page.dialog = confirmation_dialog
        confirmation_dialog.open = True
        page.update()

    def close_dialog(dialog):
        """Close a dialog."""
        dialog.open = False
        page.update()

    # Input components
    guest_name_input = ft.TextField(label="Nama Tamu", autofocus=True)
    rsvp_status_input = ft.Dropdown(
        label="Status RSVP",
        options=[
            ft.dropdown.Option("Hadir"),
            ft.dropdown.Option("Tidak Hadir"),
            ft.dropdown.Option("Menyusul"),
        ],
    )

    # Main UI
    page.add(
        ft.Column(
            [
                ft.Container(
                content=ft.Text(
                    "PlanPal", size=40, weight=ft.FontWeight.BOLD,color="#FFF5E9"
                ),
                bgcolor="#4539B4",  # Warna latar belakang biru
                padding=ft.padding.symmetric(horizontal=16, vertical=6),  # Memberikan padding
                alignment=ft.alignment.center_left,
                expand=True # Membuatnya meluas ke seluruh lebar layar
                ),
                ft.Row([
                    ft.Text("Daftar Tamu", size=30, weight=ft.FontWeight.BOLD, color="#4539B4"),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([ft.ElevatedButton(
                    content=ft.Text("Tambah", weight=ft.FontWeight.BOLD, color="#4539B4"),
                    on_click=add_guest
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(),
                guest_list_container,
                ft.Row([
                    previous_button,
                    ft.Text(f"Page {current_page} of {len(guest_controller.guest_list) // guests_per_page + 1}", size=12),
                    next_button,
                ], alignment=ft.MainAxisAlignment.CENTER),
            ]
        )
    )
    update_ui()

ft.app(target=main)
