import flet as ft
from src.utils.buttons import *

class GuestListForm:
    def __init__(self):
        self.guest_details = None

    def display_form(self, page, on_submit, event_id, guest_id, guest_list_data=None, is_edit=False):
        print("Displaying form with guest list data:", guest_list_data)

        # Set default values if guest_list_data is None
        event_id = event_id
        guest_id = guest_id
        guest_name = guest_list_data["GuestName"] if guest_list_data else ""
        rsvp_status = guest_list_data["RSVPStatus"] if guest_list_data else ""

        # Create the dialog
        self.dialog = ft.AlertDialog(
            title=ft.Text("Edit Guest" if is_edit else "Add Guest"),
            content=ft.Column([
                # ft.TextField(label="Event ID", value=event_id, color="#4539B4"),
                ft.TextField(label="Guest Name", value=guest_name, color="#4539B4"),
                ft.Dropdown(label="RSVP Status", 
                            options=[
                            ft.dropdown.Option("Hadir"), 
                            ft.dropdown.Option("Tidak Hadir"), 
                            ft.dropdown.Option("Menyusul"),
                            ft.dropdown.Option("Meninggalkan")
                            ], 
                            value=rsvp_status, color="#4539B4"),
                ],
                height=300,
            ),
            actions=[
                SaveButton(on_click_action=lambda e: self.submit_form(page, event_id, guest_id, on_submit, is_edit)),
                CancelButton(on_click_action=lambda e: self.close_dialog(page)),
            ]
        )
        page.dialog = self.dialog
        self.dialog.open = True
        page.update()

    def submit_form(self, page, event_id, guest_id, on_submit, is_edit):
        """Handle form submission by validating and passing data to the controller."""
        print("Submitting form...")
        try:
            # Collecting values from the form
            event_id = event_id
            guest_id = guest_id
            # if isinstance(event_id, int):
            #     pass
            # elif event_id.isdigit():
            #     event_id = int(event_id)  # Convert it to an integer if it's a string
            # else:
            #     raise ValueError("Event ID must be a valid number.")

            form_data = {
                # "EventID": int(event_id),
                "GuestName": self.dialog.content.controls[0].value,
                "RSVPStatus": self.dialog.content.controls[1].value,
            }

            # Validate the form data
            if self.validate_form_data(form_data):
                self.guest_details = form_data  # Store the form data

                # Close the dialog once the data is valid
                self.close_dialog(page)
                print("Form data is valid, calling on_submit")

                # If editing, we update the existing entry; if adding, we add a new entry
                if is_edit:
                    print(f"Editing guest for EventID: {event_id}")
                    on_submit(form_data, is_edit, event_id, guest_id)  # Update existing entry
                else:
                    print("Adding new guest")
                    on_submit(form_data, is_edit, event_id, guest_id)  # Add new entry
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
        required_fields = ["GuestName", "RSVPStatus"]
        for field in required_fields:
            if field not in form_data or not form_data[field]:
                self.display_error_message(f"Field '{field}' cannot be empty.")
                return False
        return True

    