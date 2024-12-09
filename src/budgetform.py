import flet as ft

class BudgetForm:
    def __init__(self):
        self.budget_details = None

    def display_form(self, page, on_submit, budget_data=None, is_edit=False, original_event_id=None):
        print("Displaying form with budget data:", budget_data)
        
        self.dialog = ft.AlertDialog(
            title=ft.Text("Edit Budget" if is_edit else "Add Budget"),
            content=ft.Column([
                ft.TextField(label="Event ID", value=budget_data["EventID"] if budget_data else "", on_change=self.validate_integer),
                ft.TextField(label="Requirement Name", value=budget_data["RequirementName"] if budget_data else ""),
                ft.TextField(label="Budget per Unit", value=str(budget_data["RequirementBudget"]) if budget_data else ""),
                ft.TextField(label="Quantity", value=str(budget_data["RequirementQuantity"]) if budget_data else ""),
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
            e.control.error_text = "This field must be a number."
        else:
            e.control.error_text = None
        e.control.update()

    def submit_form(self, page, on_submit, is_edit, original_event_id):
        print("Submitting form")
        try:
            event_id = self.dialog.content.controls[0].value
            if not event_id.isdigit():
                raise ValueError("Event ID must be a number.")
            
            form_data = {
                "EventID": int(event_id),
                "RequirementName": self.dialog.content.controls[1].value,
                "RequirementBudget": float(self.dialog.content.controls[2].value),
                "RequirementQuantity": int(self.dialog.content.controls[3].value),
            }

            if self.validate_form_data(form_data):
                self.budget_details = form_data
                self.close_dialog(page)  
                print("Form data is valid, calling on_submit")
                on_submit(form_data, is_edit, original_event_id)
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
        required_fields = ["EventID", "RequirementName", "RequirementBudget", "RequirementQuantity"]
        for field in required_fields:
            if field not in form_data or not form_data[field]:
                self.display_error_message(f"Field '{field}' cannot be empty.")
                return False
        return True
