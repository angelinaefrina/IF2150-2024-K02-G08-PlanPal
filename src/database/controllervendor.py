from .database import VendorDatabase

class ControllerVendor:
    def __init__(self, vendor_db):
        self.vendor_db = vendor_db

    def add_vendor(self, event_id, vendor_name, vendor_contact, vendor_product):
        vendor_data = {
            "EventID": event_id,
            "VendorName": vendor_name,
            "VendorContact": vendor_contact,
            "VendorProduct": vendor_product
        }
        if self.validate_vendor(vendor_data):
            self.vendor_db.add_vendor(event_id, vendor_name, vendor_contact, vendor_product)
            print(f"Vendor '{vendor_name}' berhasil ditambahkan untuk EventID {event_id}.")
        else:
            print("Gagal menambahkan vendor. Data tidak valid.")

    def edit_vendor(self, event_id, vendor_name, vendor_contact, vendor_product):
        vendor_data = {
            "EventID": event_id,
            "VendorName": vendor_name,
            "VendorContact": vendor_contact,
            "VendorProduct": vendor_product
        }

        if self.validate_vendor(vendor_data):
            # self.vendor_db.update_vendor(vendor_data)
            self.vendor_db.delete_vendor(event_id, vendor_name, vendor_contact, vendor_product)
            self.vendor_db.add_vendor(event_id, vendor_name, vendor_contact, vendor_product)
            print(f"Vendor '{vendor_name}' berhasil diperbarui untuk EventID {event_id}.")
        else:
            print("Gagal memperbarui vendor. Data tidak valid.")

    def validate_vendor(self, vendor_data):
        required_fields = ["EventID", "VendorName", "VendorContact", "VendorProduct"]
        for field in required_fields:
            if field not in vendor_data or not vendor_data[field]:
                print(f"Validasi gagal: '{field}' harus diisi.")
                return False

        return True

    def delete_vendor(self, event_id, vendor_name):
        if self.vendor_db.delete_vendor(event_id, vendor_name):
            print(f"Vendor '{vendor_name}' berhasil dihapus dari EventID {event_id}.")
        else:
            print(f"Vendor '{vendor_name}' tidak ditemukan untuk EventID {event_id}.")

    def get_vendor_by_event_id(self, event_id):
        vendors = self.vendor_db.get_vendors_by_event(event_id)
        if not vendors:
            print(f"Tidak ada vendor yang ditemukan untuk EventID {event_id}.")
        return vendors
    
    def get_all_vendors(self):
        vendors = self.vendor_db.select_all_vendors()

        if not vendors:
            print(f"Tidak ada vendor yang ditemukan.")
        return vendors