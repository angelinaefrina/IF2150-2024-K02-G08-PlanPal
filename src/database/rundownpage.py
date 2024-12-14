import flet as ft
from src.utils.buttons import *

class RundownPage:
    def __init__(self):
        self.rundown_details = None

    def display_form(self, page, on_submit, event_id, rundown_data=None, is_edit=False, original_event_id=None):
        if not callable(on_submit):
            raise TypeError("on_submit must be a callable function.")
        
        print("Displaying rundown form with rundown data...", rundown_data)

        # Set default
        event_id = event_id
        agenda_name = rundown_data["AgendaName"] if rundown_data else ""
        agenda_time_start = rundown_data["AgendaTimeStart"] if rundown_data else ""
        agenda_time_end = rundown_data["AgendaTimeEnd"] if rundown_data else ""
        agenda_pic = rundown_data["AgendaPIC"] if rundown_data else ""

        # Create the dialog
        self.dialog = ft.AlertDialog(
            title=ft.Text("Edit Rundown" if is_edit else "Add Rundown"),
            content=ft.Column([
                # ft.TextField(label="Event ID", value=event_id, color="#4539B4", on_change=self.validate_integer),
                ft.TextField(label="Agenda Name", value=agenda_name, color="#4539B4"),
                ft.TextField(label="Start Time (HH:MM)", value=agenda_time_start, color="#4539B4"),
                ft.TextField(label="End Time (HH:MM)", value=agenda_time_end, color="#4539B4"),
                ft.TextField(label="PIC", value=agenda_pic, color="#4539B4"),
            ],
                height=300,
            ),
            actions=[
                SaveButton(on_click_action=lambda e: self.submit_form(page, on_submit, is_edit, event_id)),
                CancelButton(on_click_action=lambda e: self.close_dialog(page)),
            ]
        )
        page.dialog = self.dialog # Set the dialog on the page
        self.dialog.open = True # Open the dialog
        page.update()

    def validate_integer(self, e):
        if not e.control.value.isdigit():
            e.control.error_text = "This field must be a number."
        else:
            e.control.error_text = None
        e.control.update()

    def validate_time_format(self, time_string):
        from datetime import datetime
        try:
            datetime.strptime(time_string, "%H:%M")
            return True
        except ValueError:
            return False

    def submit_form(self, page, on_submit, is_edit, event_id):
        print("Submitting form...")
        try:
            # Collecting values from the form
            # event_id = event_id
            # if isinstance(event_id, int):
            #     pass
            # elif event_id.isdigit():
            #     event_id = int(event_id)  # Convert it to an integer if it's a string
            # else:
            #     raise ValueError("Event ID must be a valid number.")

            form_data = {
                "EventID": event_id,
                "AgendaName": self.dialog.content.controls[0].value,
                "AgendaTimeStart": self.dialog.content.controls[1].value,
                "AgendaTimeEnd": self.dialog.content.controls[2].value,
                "AgendaPIC": self.dialog.content.controls[3].value,
            }

            # Validasi waktu
            if not self.validate_time_format(form_data["AgendaTimeStart"]) or not self.validate_time_format(form_data["AgendaTimeEnd"]):
                self.display_error_message("Invalid time format. Use HH:MM.")
                return

            # Validate the form data
            if self.validate_form_data(form_data):
                self.rundown_details = form_data  # Store the form data

                # Close the dialog once the data is valid
                self.close_dialog(page)
                print("Form data is valid, calling on_submit")

                # If editing, we update the existing entry; if adding, we add a new entry
                if is_edit:
                    on_submit(form_data, is_edit, event_id)
                else:
                    on_submit(form_data, is_edit, event_id)
            else:
                self.display_error_message("Invalid form data. Please check the form and try again.")
        except ValueError as e:
            self.display_error_message(str(e))

    def close_dialog(self, page):
        self.dialog.open = False  
        page.update()  

    def display_error_message(self, message):
        self.dialog.content.controls.append(ft.Text(message, color=ft.colors.RED))
        self.dialog.update()

    def validate_form_data(self, form_data):
        required_fields = ["EventID", "AgendaName", "AgendaTimeStart", "AgendaTimeEnd", "AgendaPIC"]
        for field in required_fields:
            if field not in form_data or not form_data[field]:
                self.display_error_message(f"Field '{field}' is required.")
                return False
        return True
