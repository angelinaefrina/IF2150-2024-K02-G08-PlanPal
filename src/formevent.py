import flet as ft

class FormEvent:
    def __init__(self):
        self.event_details = None

    def display_form(self, page, on_submit, event_data=None, is_edit=False, original_event_id=None):
        print("Displaying form with event data:", event_data)
        self.dialog = ft.AlertDialog(
            title=ft.Text("Edit Event" if is_edit else "Add Event"),
            content=ft.Column([
                ft.TextField(label="Event ID", value=event_data["EventID"] if event_data else "", on_change=self.validate_integer),
                ft.TextField(label="Event Location", value=event_data["EventLocation"] if event_data else ""),
                ft.TextField(label="Event Date (YYYY-MM-DD)", value=event_data["EventDate"] if event_data else ""),
                ft.Dropdown(
                    label="Event Status",
                    options=[
                        ft.dropdown.Option("Belum dimulai"),
                        ft.dropdown.Option("Sedang berlangsung"),
                        ft.dropdown.Option("Sudah selesai")
                    ],
                    value=event_data["EventStatus"] if event_data else ""
                ),
            ]),
            actions=[
                ft.TextButton("Submit", on_click=lambda e: self.submit_form(page, on_submit, is_edit, original_event_id)),
                ft.TextButton("Cancel", on_click=lambda e: self.close_dialog(page))
            ]
        )
        page.dialog = self.dialog  # Set the dialog on the page
        self.dialog.open = True  # Open the dialog
        page.update()  # Update the page to reflect changes

    def validate_integer(self, e):
        if not e.control.value.isdigit():
            e.control.error_text = "Event ID harus berupa angka."
        else:
            e.control.error_text = None
        e.control.update()

    def submit_form(self, page, on_submit, is_edit, original_event_id):
        print("Submitting form")
        try:
            event_id = self.dialog.content.controls[0].value
            if not event_id.isdigit():
                raise ValueError("Event ID harus berupa angka.")
            
            form_data = {
                "EventID": int(event_id),
                "EventLocation": self.dialog.content.controls[1].value,
                "EventDate": self.dialog.content.controls[2].value,
                "EventStatus": self.dialog.content.controls[3].value
            }
            if self.validate_form_data(form_data):
                self.event_details = form_data
                self.close_dialog(page)  # Close the dialog
                print("Form data is valid, calling on_submit")
                on_submit(form_data, is_edit, original_event_id)
            else:
                self.display_error_message("Data form tidak valid.")
        except ValueError as e:
            self.display_error_message(str(e))

    def close_dialog(self, page):
        self.dialog.open = False  # Close the dialog
        page.update()  # Update the page to reflect changes

    def display_error_message(self, message):
        self.dialog.content.controls.append(ft.Text(message, color=ft.colors.RED))
        self.dialog.update()

    def validate_form_data(self, form_data):
        required_fields = ["EventID", "EventLocation", "EventDate", "EventStatus"]
        for field in required_fields:
            if field not in form_data or not form_data[field]:
                self.display_error_message(f"Field '{field}' tidak boleh kosong.")
                return False
        return True