class VendorPage:
    def __init__(self, controller_vendor):
        self.controller_vendor = controller_vendor

    def display_form(self):
        print("\n=== Form Tambah Vendor ===")
        event_id = input("Masukkan Event ID: ")
        vendor_name = input("Masukkan Nama Vendor: ")
        vendor_contact = input("Masukkan Kontak Vendor: ")
        vendor_product = input("Masukkan Produk/Jasa Vendor: ")
        return event_id, vendor_name, vendor_contact, vendor_product

    def submit_form(self):
        event_id, vendor_name, vendor_contact, vendor_product = self.display_form()
        try:
            event_id = int(event_id)
            self.controller_vendor.add_vendor(event_id, vendor_name, vendor_contact, vendor_product)
        except ValueError:
            self.display_error("Event ID harus berupa angka.")

    def display_error(self, message):
        print(f"\n[Error]: {message}")

    def display_vendor(self, event_id):
        print(f"\n=== Daftar Vendor untuk EventID {event_id} ===")
        try:
            event_id = int(event_id)
            vendors = self.controller_vendor.get_vendor_by_event_id(event_id)

            if not vendors:
                print("Tidak ada vendor yang terdaftar untuk event ini.")
                return

            for idx, vendor in enumerate(vendors, start=1):
                print(
                    f"{idx}. Nama: {vendor['VendorName']}, "
                    f"Kontak: {vendor['VendorContact']}, "
                    f"Produk/Jasa: {vendor['VendorProduct']}"
                )
        except ValueError:
            self.display_error("Event ID harus berupa angka.")