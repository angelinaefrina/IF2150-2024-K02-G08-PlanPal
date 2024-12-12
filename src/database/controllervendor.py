class ControllerVendor:
    def __init__(self):
        self.vendor_database = []

    def add_vendor(self, event_id, vendor_name, vendor_contact, vendor_product):
        vendor_data = {
            "EventID": event_id,
            "VendorName": vendor_name,
            "VendorContact": vendor_contact,
            "VendorProduct": vendor_product
        }

        if self.validate_vendor(vendor_data):
            self.vendor_database.append(vendor_data)
            print(f"Vendor '{vendor_name}' berhasil ditambahkan untuk EventID {event_id}.")
        else:
            print("Gagal menambahkan vendor. Data tidak valid.")

    def validate_vendor(self, vendor_data):
        required_fields = ["EventID", "VendorName", "VendorContact", "VendorProduct"]
        for field in required_fields:
            if field not in vendor_data or not vendor_data[field]:
                print(f"Validasi gagal: '{field}' harus diisi.")
                return False

        return True

    def delete_vendor(self, event_id, vendor_name):
        for vendor in self.vendor_database:
            if vendor["EventID"] == event_id and vendor["VendorName"] == vendor_name:
                self.vendor_database.remove(vendor)
                print(f"Vendor '{vendor_name}' berhasil dihapus dari EventID {event_id}.")
                return
        print(f"Vendor '{vendor_name}' tidak ditemukan untuk EventID {event_id}.")

    def get_vendor_by_event_id(self, event_id):
        vendors = [vendor for vendor in self.vendor_database if vendor["EventID"] == event_id]

        if not vendors:
            print(f"Tidak ada vendor yang ditemukan untuk EventID {event_id}.")
        return vendors
    
    def get_all_vendor(self):
        vendors = [vendor for vendor in self.vendor_database]

        if not vendors:
            print(f"Tidak ada vendor yang ditemukan.")
        return vendors
