import flet as ft
from src.utils.buttons import *

class BudgetForm:
    def __init__(self):
        self.budget_details = None

    def display_form(self, page, on_submit, budget_data=None, is_edit=False, original_event_id=None):
        print("Displaying form with budget data:", budget_data)
        
        # Set default values if budget_data is None
        event_id = str(budget_data["EventID"]) if budget_data else ""
        requirement_name = budget_data["RequirementName"] if budget_data else ""
        requirement_budget = str(budget_data["RequirementBudget"]) if budget_data else ""
        requirement_quantity = str(budget_data["RequirementQuantity"]) if budget_data else ""

        # Create the dialog
        self.dialog = ft.AlertDialog(
            title=ft.Text("Edit Budget" if is_edit else "Add Budget"),
            content=ft.Column([
                ft.TextField(label="Event ID", value=event_id, color="#4539B4", on_change=self.validate_integer),
                ft.TextField(label="Requirement Name", value=requirement_name, color="#4539B4"),
                ft.TextField(label="Budget per Unit", value=requirement_budget, color="#4539B4"),
                ft.TextField(label="Quantity", value=requirement_quantity, color="#4539B4"),
            ],
                height=300,
            ),
            actions=[
                SaveButton(on_click_action=lambda e: self.submit_form(page, on_submit, is_edit, original_event_id)),
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

    def submit_form(self, page, on_submit, is_edit, original_event_id):
        """Handle form submission by validating and passing data to the controller."""
        print("Submitting form...")
        try:
            # Collecting values from the form
            event_id = self.dialog.content.controls[0].value
            if isinstance(event_id, int):
                pass
            elif event_id.isdigit():
                event_id = int(event_id)  # Convert it to an integer if it's a string
            else:
                raise ValueError("Event ID must be a valid number.")

            form_data = {
                "EventID": int(event_id),
                "RequirementName": self.dialog.content.controls[1].value,
                "RequirementBudget": float(self.dialog.content.controls[2].value),
                "RequirementQuantity": int(self.dialog.content.controls[3].value),
            }

            # Validate the form data
            if self.validate_form_data(form_data):
                self.budget_details = form_data  # Store the form data

                # Close the dialog once the data is valid
                self.close_dialog(page)
                print("Form data is valid, calling on_submit")

                # If editing, we update the existing entry; if adding, we add a new entry
                if is_edit:
                    print(f"Editing budget for EventID: {original_event_id}")
                    on_submit(form_data, is_edit, original_event_id)  # Update existing entry
                else:
                    print("Adding new budget")
                    on_submit(form_data, is_edit, original_event_id=None)  # Add new entry
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
