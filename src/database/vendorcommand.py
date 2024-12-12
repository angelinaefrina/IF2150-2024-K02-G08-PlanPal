class VendorCommand:
    def __init__(self, vendor_page):
        self.vendor_page = vendor_page

    def display_commands(self):
        print("\n=== Vendor Management Commands ===")
        print("1. Add Vendor")
        print("2. Edit Vendor")
        print("3. Delete Vendor")
        print("4. Exit")
        print("\nEnter the number of the action you want to perform.")
