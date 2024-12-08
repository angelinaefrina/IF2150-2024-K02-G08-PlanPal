import flet as ft

class GuestListForm(ft.UserControl):
    def __init__(self, add_guest_callback, edit_guest_callback, delete_guest_callback):
        super().__init__()
        self.add_guest_callback = add_guest_callback
        self.edit_guest_callback = edit_guest_callback
        self.delete_guest_callback = delete_guest_callback

    def build(self):
        self.guest_name_input = ft.TextField(label="Nama Tamu", autofocus=True)
        self.rsvp_status_input = ft.Dropdown(options=["Hadir", "Tidak Hadir", "Menyusul"], label="RSVP Status")
        self.add_button = ft.ElevatedButton("Tambah Tamu", on_click=self.add_guest)
        self.edit_button = ft.ElevatedButton("Edit Tamu", on_click=self.edit_guest)
        self.delete_button = ft.ElevatedButton("Hapus Tamu", on_click=self.delete_guest)

        return ft.Column([
            self.guest_name_input,
            self.rsvp_status_input,
            self.add_button,
            self.edit_button,
            self.delete_button,
        ])

    def add_guest(self, e):
        guest_name = self.guest_name_input.value
        rsvp_status = self.rsvp_status_input.value
        self.add_guest_callback(self.page, guest_name, rsvp_status)

    def edit_guest(self, e):
        guest_name = self.guest_name_input.value
        rsvp_status = self.rsvp_status_input.value
        self.edit_guest_callback(self.page, guest_name, rsvp_status)

    def delete_guest(self, e):
        guest_name = self.guest_name_input.value
        self.delete_guest_callback(self.page, guest_name)
