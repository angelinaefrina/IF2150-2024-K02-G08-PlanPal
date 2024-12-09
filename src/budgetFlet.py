import flet as ft
from budgetcontroller import ControllerBudget
from budgetform import BudgetForm

class BudgetManagerApp:
    def __init__(self, page):
        self.page = page
        self.page.title = "Budget Management"

        self.page.bgcolor = ft.colors.with_opacity(1, '#f5e8d9')

        self.controller = ControllerBudget()
        self.budget_form = BudgetForm()

        self.controller.add_budget(1, "Benda A", 1000, 10)
        self.controller.add_budget(2, "Benda B", 2000, 5)

        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        self.tree = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Event ID", color= "#4539B4")),
                ft.DataColumn(ft.Text("Nama", color= "#4539B4")),
                ft.DataColumn(ft.Text("Harga Satuan", color= "#4539B4")),
                ft.DataColumn(ft.Text("Jumlah", color= "#4539B4")),
                ft.DataColumn(ft.Text("Total", color= "#4539B4")),
                ft.DataColumn(ft.Text("")),
            ],
            rows=[],
        )
        self.title = ft.Text("Anggaran", size=30, weight=ft.FontWeight.BOLD, color= "#4539B4")
        self.add_button = ft.ElevatedButton(text="Add Budget", color= "#4539B4", on_click=self.add_budget)
        self.page.add(
            ft.Column(
                controls=[
                    self.title,
                    self.add_button,
                    self.tree  # Add the table below the button
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Center horizontally
            )
        )
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
                                        color= "#4539B4",
                                        on_click=lambda e, event_id=budget["EventID"], requirement_name=budget["RequirementName"]: self.edit_budget(event_id, requirement_name)
                                    ),
                                    ft.ElevatedButton(
                                        text="Delete", 
                                        color= "#4539B4",
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
        budgets = self.controller.get_budget_list(event_id)

        print(f"Budgets retrieved for EventID {event_id}: {budgets}")

        # cek kalau data tidak ada
        if not budgets:
            print(f"No budgets found for EventID {event_id}.")
            self.show_error_dialog(f"No budgets found for Event ID '{event_id}'.")
            return

        budget_data = next((budget for budget in budgets if budget["RequirementName"] == requirement_name), None)

        if budget_data:
            # data ketemu
            self.budget_form.display_form(self.page, self.on_form_submit, budget_data, is_edit=True, original_event_id=event_id)
        else:
            print(f"No budget found for EventID {event_id} and RequirementName {requirement_name}")
            self.show_error_dialog(f"Budget with Event ID '{event_id}' and Requirement Name '{requirement_name}' not found.")

    def delete_budget(self, event_id, requirement_name):
        if self.controller.get_budget_list(event_id):
            self.controller.delete_budget(event_id, requirement_name)
            self.update_display()  
        else:
            self.show_error_dialog(f"Budget with Event ID '{event_id}' and Requirement Name '{requirement_name}' not found.")


def main(page: ft.Page):
    app = BudgetManagerApp(page)

ft.app(target=main)