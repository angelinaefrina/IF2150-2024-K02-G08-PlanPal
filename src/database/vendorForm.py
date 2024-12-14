import flet as ft
from src.utils.buttons import *

class VendorForm:
    def __init__(self):
        self.vendor_details = None

    def display_form(self, page, on_submit, event_id, vendor_data=None, is_edit=False):
        print("Displaying form with vendor data:", vendor_data)

        # Set default values if vendor_data is None
        event_id = event_id
        vendor_name = vendor_data["VendorName"] if vendor_data else ""
        vendor_contact = vendor_data["VendorContact"] if vendor_data else ""
        vendor_product = vendor_data["VendorProduct"] if vendor_data else ""

        # Create the dialog
        self.dialog = ft.AlertDialog(
            title=ft.Text("Edit Vendor" if is_edit else "Add Vendor"),
            content=ft.Column([
                # ft.TextField(label="Event ID", value=event_id, color="#4539B4", on_change=self.validate_integer),
                ft.TextField(label="Vendor Name", value=vendor_name, color="#4539B4"),
                ft.TextField(label="Contact", value=vendor_contact, color="#4539B4"),
                ft.TextField(label="Product/Service", value=vendor_product, color="#4539B4"),
            ],
                height=300,
            ),
            actions=[
                SaveButton(on_click_action=lambda e: self.submit_form(page, event_id, on_submit, is_edit)),
                CancelButton(on_click_action=lambda e: self.close_dialog(page)),
            ]
        )
        page.dialog = self.dialog  # Set the dialog on the page
        self.dialog.open = True  # Open the dialog
        page.update()  # Update the page to reflect changes

    def validate_integer(self, e):
        if not e.control.value.isdigit():
            e.control.error_text = "This field must be a number."
        else:
            e.control.error_text = None
        e.control.update()

    def submit_form(self, page, event_id, on_submit, is_edit):
        """Handle form submission by validating and passing data to the controller."""
        print("Submitting form...")
        try:
            # Collecting values from the form
            event_id = event_id
            # if isinstance(event_id, int):
            #     pass
            # elif event_id.isdigit():
            #     event_id = int(event_id)  # Convert it to an integer if it's a string
            # else:
            #     raise ValueError("Event ID must be a valid number.")

            form_data = {
                # "EventID": int(event_id),
                "VendorName": self.dialog.content.controls[0].value,
                "VendorContact": self.dialog.content.controls[1].value,
                "VendorProduct": self.dialog.content.controls[2].value,
            }

            # Validate the form data
            if self.validate_form_data(form_data):
                self.vendor_details = form_data  # Store the form data

                # Close the dialog once the data is valid
                self.close_dialog(page)
                print("Form data is valid, calling on_submit")

                # If editing, we update the existing entry; if adding, we add a new entry
                if is_edit:
                    print(f"Editing vendor for EventID: {event_id}")
                    on_submit(form_data, is_edit, event_id)  # Update existing entry
                else:
                    print("Adding new vendor")
                    on_submit(form_data, is_edit, event_id)  # Add new entry
            else:
                self.display_error_message("Form data is invalid.")
        except ValueError as e:
            self.display_error_message(str(e))

    def close_dialog(self, page):
        self.dialog.open = False
        page.update()

    def display_error_message(self, message):
        self.dialog.content.controls.append(ft.Text(message, color=ft.colors.RED))
        self.dialog.update()

    def validate_form_data(self, form_data):
        # Ensure that all required fields are filled out
        required_fields = ["VendorName", "VendorContact", "VendorProduct"]
        for field in required_fields:
            if field not in form_data or not form_data[field]:
                self.display_error_message(f"Field '{field}' cannot be empty.")
                return False
        return True