import flet as ft
from guestcontroller import GuestController

# lanjut besok ya ef maaf gakuat ngantuk banget

def main(page: ft.Page):
    page.title = "PlanPal - Daftar Tamu"
    page.scroll = ft.ScrollMode.AUTO

    guest_controller = GuestController()
    current_page = 1
    rows_per_page = 10

    def refresh_table():
        guest_table.rows.clear()
        start_idx = (current_page - 1) * rows_per_page
        end_idx = start_idx + rows_per_page
        for guest in guest_controller.guest_list[start_idx:end_idx]:
            guest_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(guest["GuestName"])),
                        ft.DataCell(ft.Text(guest["RSVPStatus"])),
                    ]
                )
            )
        update_page_label()
        page.update()

    def update_page_label():
        total_pages = max(1, -(-len(guest_controller.guest_list) // rows_per_page))
        page_label.value = f"Page {current_page} of {total_pages}"
        page.update()

    def show_guest_form(edit_mode=False, guest_data=None):
        def save_guest():
            guest_name = guest_name_field.value.strip()
            rsvp_status = rsvp_dropdown.value
            if edit_mode:
                guest_data["GuestName"] = guest_name
                guest_data["RSVPStatus"] = rsvp_status
            else:
                guest_controller.add_guest_list(len(guest_controller.guest_list) + 1, guest_name, rsvp_status)
            dialog.open = False
            refresh_table()
            page.update()

        guest_name_field.value = guest_data["GuestName"] if guest_data else ""
        rsvp_dropdown.value = guest_data["RSVPStatus"] if guest_data else "Accepted"
        
        # Adding save button that triggers save_guest on click
        save_button = ft.TextButton("Simpan", on_click=save_guest)  
        cancel_button = ft.TextButton("Batal", on_click=lambda e: dialog.close())
        
        dialog.content = ft.Column([guest_name_field, rsvp_dropdown, save_button, cancel_button])
        dialog.open = True
        page.update()


    def delete_guest():
        if len(guest_controller.guest_list) > 0:
            guest_controller.guest_list.pop()
            refresh_table()

    # Components
    guest_name_field = ft.TextField(label="Nama Tamu")
    rsvp_dropdown = ft.Dropdown(
        label="RSVP Status",
        options=[
            ft.dropdown.Option("Accepted"),
            ft.dropdown.Option("Declined"),
            ft.dropdown.Option("Pending"),
        ],
    )

    # Adding guest_table, page_label, and dialog components
    guest_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nama")),
            ft.DataColumn(ft.Text("Status")),
        ],
        rows=[],
    )

    page_label = ft.Text("Page 1 of 1")

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Detail Tamu"),
        content=ft.Column([guest_name_field, rsvp_dropdown]),
        actions=[
            ft.TextButton("Simpan", on_click=save_guest()),
            ft.TextButton("Batal", on_click=lambda e: setattr(dialog, "open", False)),
        ],
    )

    # Adding components to the page
    page.add(
        ft.Column(
            [
                ft.Row([ft.Text("Daftar Tamu", style="headlineMedium"), page_label]),
                guest_table,
                ft.Row(
                    [
                        ft.FilledButton("Tambah", on_click=lambda e: show_guest_form(edit_mode=False)),
                        ft.FilledButton("Edit", on_click=lambda e: print("Edit not yet implemented")),
                        ft.FilledButton("Hapus", on_click=delete_guest),
                    ],
                    alignment="spaceEvenly",
                ),
            ]
        ),
        dialog,
    )

    # Initialize the table on the first load
    refresh_table()
