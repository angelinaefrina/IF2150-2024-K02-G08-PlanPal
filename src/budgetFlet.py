import flet as ft
from budgetcontroller import ControllerBudget
from budgetform import BudgetForm

class BudgetManagerApp:
    def __init__(self, page):
        self.page = page
        self.page.title = "Budget Management"

        self.controller = ControllerBudget()
        self.budget_form = BudgetForm()

        self.controller.add_budget(1, "Location A", 1000, 10)
        self.controller.add_budget(2, "Location B", 2000, 5)

        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        self.tree = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Event ID")),
                ft.DataColumn(ft.Text("Requirement")),
                ft.DataColumn(ft.Text("Budget/Unit")),
                ft.DataColumn(ft.Text("Quantity")),
                ft.DataColumn(ft.Text("Total Cost")),
                ft.DataColumn(ft.Text("Actions")),
            ],
            rows=[],
        )

        self.add_button = ft.ElevatedButton(text="Add Budget", on_click=self.add_budget)

        self.page.add(self.tree, self.add_button)

    def add_budget(self, e):
        self.budget_form.display_form(self.page, self.on_form_submit, is_edit=False)

    def on_form_submit(self, form_data, is_edit, original_event_id):
        if is_edit:
            self.controller.edit_budget(original_event_id, form_data["RequirementName"], form_data["RequirementBudget"], form_data["RequirementQuantity"])
        else:
            self.controller.add_budget(
                form_data["EventID"], 
                form_data["RequirementName"], 
                form_data["RequirementBudget"], 
                form_data["RequirementQuantity"]
            )
        self.update_display()

    def update_display(self):
        self.tree.rows.clear()  
        for budget in self.controller.get_all_budget_list():
            total_cost = budget["RequirementBudget"] * budget["RequirementQuantity"]
            self.tree.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(budget["EventID"])),
                        ft.DataCell(ft.Text(budget["RequirementName"])),
                        ft.DataCell(ft.Text(budget["RequirementBudget"])),
                        ft.DataCell(ft.Text(budget["RequirementQuantity"])),
                        ft.DataCell(ft.Text(total_cost)),
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    ft.ElevatedButton(
                                        text="Edit", 
                                        on_click=lambda e, event_id=budget["EventID"], requirement_name=budget["RequirementName"]: self.edit_budget(event_id, requirement_name)
                                    ),
                                    ft.ElevatedButton(
                                        text="Delete", 
                                        on_click=lambda e, event_id=budget["EventID"], requirement_name=budget["RequirementName"]: self.delete_budget(event_id, requirement_name)
                                    ),
                                ]
                            )
                        ),
                    ]
                )
            )
        self.page.update()


    def edit_budget(self, event_id, requirement_name):
        budget_data = self.controller.get_budget_list(self, event_id)
        if budget_data and budget_data["RequirementName"] == requirement_name:
            self.form_budget.display_form(self.page, self.on_form_submit, budget_data, is_edit=True, original_event_id=event_id)
        else:
            self.show_error_dialog(f"Budget with Event ID '{event_id}' and Requirement Name '{requirement_name}' not found.")

    def delete_budget(self, event_id, requirement_name):
        if self.controller.get_budget_list(self,event_id):
            self.controller.delete_budget(event_id, requirement_name)
            self.update_display()  
        else:
            self.show_error_dialog(f"Budget with Event ID '{event_id}' and Requirement Name '{requirement_name}' not found.")


def main(page: ft.Page):
    app = BudgetManagerApp(page)

ft.app(target=main)