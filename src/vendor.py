class Vendor:
    def __init__(self, event_id, vendor_name, vendor_contact, vendor_product):
        self.event_id = event_id
        self.vendor_name = vendor_name
        self.vendor_contact = vendor_contact
        self.vendor_product = vendor_product

    def get_vendor_name(self):
        return self.vendor_name

    def get_vendor_contact(self):
        return self.vendor_contact

    def get_vendor_product(self):
        return self.vendor_product

    def set_vendor_name(self, vendor_name):
        self.vendor_name = vendor_name

    def set_vendor_contact(self, vendor_contact):
        self.vendor_contact = vendor_contact

    def set_vendor_product(self, vendor_product):
        self.vendor_product = vendor_product