import flet as ft

class VendorPage(ft.UserControl):
    def __init__(self, controller_vendor):
        self.controller_vendor = controller_vendor
        super().__init__()

    def build(self):
        self.event_id_input = ft.TextField(label="Event ID")
        self.vendor_name_input = ft.TextField(label="Nama Vendor")
        self.vendor_contact_input = ft.TextField(label="Kontak Vendor")
        self.vendor_product_input = ft.TextField(label="Produk/Jasa Vendor")
        
        self.submit_button = ft.ElevatedButton(text="Tambah Vendor", on_click=self.submit_form)
        self.view_button = ft.ElevatedButton(text="Lihat Vendor", on_click=self.view_vendor)
        
        self.vendor_listbox = ft.ListView(expand=True)

        return ft.Column(
            controls=[
                self.event_id_input,
                self.vendor_name_input,
                self.vendor_contact_input,
                self.vendor_product_input,
                self.submit_button,
                self.view_button,
                self.vendor_listbox
            ]
        )

    def submit_form(self, e):
        event_id = self.event_id_input.value
        vendor_name = self.vendor_name_input.value
        vendor_contact = self.vendor_contact_input.value
        vendor_product = self.vendor_product_input.value
        
        if not event_id or not vendor_name or not vendor_contact or not vendor_product:
            self.show_error("Semua kolom harus diisi.")
            return

        try:
            event_id = int(event_id)
            self.controller_vendor.add_vendor(event_id, vendor_name, vendor_contact, vendor_product)
            self.show_message("Sukses", "Vendor berhasil ditambahkan")
            self.clear_form()
        except ValueError:
            self.show_error("Event ID harus berupa angka.")

    def view_vendor(self, e):
        event_id = self.event_id_input.value
        if not event_id:
            self.show_error("Masukkan Event ID terlebih dahulu.")
            return

        try:
            event_id = int(event_id)
            vendors = self.controller_vendor.get_vendor_by_event_id(event_id)
            self.vendor_listbox.controls.clear()

            if not vendors:
                self.vendor_listbox.controls.append(ft.Text("Tidak ada vendor yang terdaftar untuk event ini."))
            else:
                for vendor in vendors:
                    display_text = f"Nama: {vendor['VendorName']}, Kontak: {vendor['VendorContact']}, Produk: {vendor['VendorProduct']}"
                    self.vendor_listbox.controls.append(ft.Text(display_text))

            self.update()

        except ValueError:
            self.show_error("Event ID harus berupa angka.")

    def show_error(self, message):
        self.page.snack_bar = ft.SnackBar(ft.Text(message), open=True)
        self.update()

    def show_message(self, title, message):
        self.page.snack_bar = ft.SnackBar(ft.Text(message), open=True)
        self.update()

    def clear_form(self):
        self.event_id_input.value = ""
        self.vendor_name_input.value = ""
        self.vendor_contact_input.value = ""
        self.vendor_product_input.value = ""
        self.update()
