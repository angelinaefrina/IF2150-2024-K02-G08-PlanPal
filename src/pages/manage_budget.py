import sys
import os

# Add the src directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import flet as ft
from src.database.budget import Budget
from src.database.budgetpage import BudgetPage
from src.database.budgetform import BudgetForm
from src.database.budgetcontroller import ControllerBudget
from src.utils.cards import EventCard
from src.utils.buttons import *
from src.utils.pagesetup import PageSetup

ITEMS_PER_PAGE = 6
class BudgetManagerApp:
    def __init__(self, page):
        self.page = page
        self.page.title = "Budget Management"

        # Setup page
        self.setup_page()

        self.controller = ControllerBudget()
        self.budget_form = BudgetForm()

        self.controller.add_budget(1, "Benda A", 1000, 10)
        self.controller.add_budget(2, "Benda B", 2000, 5)

        self.current_page = 0
        self.create_widgets()
        self.update_display()

    def setup_page(self):
        width = self.page.window.width
        height = self.page.window.height
        self.page.bgcolor = '#FFF5E9'

        # Set fonts
        self.page.fonts = {
            "Header": "../src/assets/fonts/Fredoka/Fredoka-SemiBold.ttf",
            "Default_Bold": "../src/assets/fonts/Afacad/Afacad-Bold.ttf",
            "Default_Regular": "../src/assets/fonts/Afacad/Afacad-Regular.ttf",
            "Header": "../assets/fonts/Fredoka/Fredoka-SemiBold.ttf",
            "Default_Bold": "../assets/fonts/Afacad/Afacad-Bold.ttf",
            "Default_Regular": "../assets/fonts/Afacad/Afacad-Regular.ttf",
        }
        # Header PlanPal
        self.page.add(
            ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Text("PlanPal", font_family="Header", color="#FFF5E9", size=64, weight=ft.FontWeight.BOLD),
                        width=width,
                        height=100,
                        bgcolor='#4539B4',
                        padding=ft.padding.all(5),
                        alignment=ft.alignment.top_left
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )
    
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
            bgcolor="#FFF5E9",
            # border_radius= ft.border_radius.all(10),
            heading_row_color= "#FAEBD9"
        )

        self.title = ft.Text(
            value= "Anggaran", 
            size=30, 
            weight=ft.FontWeight.BOLD, 
            color= "#4539B4", 
            font_family="Default_Bold"
            )
        
        self.add_button = ft.ElevatedButton(
            text="Add Budget",
            style=ft.ButtonStyle(
                padding=ft.padding.symmetric(horizontal=20, vertical=10),
                bgcolor= "#C4E8F8",
                text_style=ft.TextStyle(
                    color= "#4539B4",
                    weight=ft.FontWeight.BOLD,
                    font_family="Default_Bold",
                    size=20,
                )
            ),
            color= "#4539B4", 
            on_click=self.add_budget
        )

        self.back_button = BackButton(
        on_click_action=self.back_to_event_manager, font_family="Default_Bold"
        )
        
        self.prev_button = ft.ElevatedButton(text="Previous", on_click=self.prev_page, disabled=True)
        self.next_button = ft.ElevatedButton(text="Next", on_click=self.next_page, disabled=True)
        
        self.page.add(
            ft.Column(
                [   
                    ft.Container(
                        content= self.title,
                        alignment= ft.alignment.center,
                        padding= ft.padding.only(bottom=10)
                    ),
                    ft.Container(
                        content= self.add_button,
                        alignment= ft.alignment.center,
                        padding= ft.padding.only(bottom=20)
                    ),
                    ft.Container(
                        content= self.tree,
                        alignment= ft.alignment.top_center,
                        expand= True
                    ),
                    ft.Row(
                        [self.prev_button, self.next_button],
                        alignment= ft.MainAxisAlignment.CENTER,
                        spacing= 20,
                    ),
                    ft.Container(
                        content=self.back_button,
                        alignment=ft.alignment.bottom_left,
                        padding=ft.padding.all(10),
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                expand=True,
            )
        )

    def add_budget(self, e):
        print("Add Budget button clicked.")
        self.budget_form.display_form(self.page, self.on_form_submit, is_edit=False)

    def back_to_event_manager(self, e):
        from src.pages.manage_event import EventManagerApp
        # Clear current page content
        self.page.controls.clear()
        # Load EventManagerApp
        EventManagerApp(self.page)
        self.page.update()


    def edit_budget(self, event_id, requirement_name):
        print("Edit Budget button clicked.")
        budgets = self.controller.get_budget_list(event_id)

        print(f"Budgets retrieved for EventID {event_id}: {budgets}")
        budget_data = next(
            (budget for budget in budgets if budget["RequirementName"] == requirement_name), None
        )

        if budget_data:
        # Display a form populated with the budget details for editing
            self.budget_form.display_form(
                page=self.page,
                on_submit=self.on_form_submit,
                budget_data=budget_data,
                is_edit=True,
                original_event_id=event_id,
            )
        else:
            self.show_error_dialog(f"Budget not found for Event ID '{event_id}' and Requirement Name '{requirement_name}'.")

    def delete_budget(self, event_id, requirement_name):
        if self.controller.get_budget_list(event_id):
            self.controller.delete_budget(event_id, requirement_name)
            self.update_display()
        else:
            self.show_error_dialog(f"Budget not found for Event ID '{event_id}' and Requirement Name '{requirement_name}'.")

    def update_display(self):
        total_pages = (len(self.controller.get_all_budget_list()) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

        self.prev_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page >= total_pages - 1

        start_index = self.current_page * ITEMS_PER_PAGE
        end_index = self.current_page + ITEMS_PER_PAGE

        total_budgets = self.controller.get_all_budget_list()
        self.tree.rows.clear()  
        for budget in total_budgets[start_index:end_index]:
            total_cost = budget["RequirementBudget"] * budget["RequirementQuantity"]
            self.tree.rows.append(
                ft.DataRow(
                    cells=
                        [
                        ft.DataCell(ft.Text(budget["EventID"])),
                        ft.DataCell(ft.Text(budget["RequirementName"])),
                        ft.DataCell(ft.Text(budget["RequirementBudget"])),
                        ft.DataCell(ft.Text(budget["RequirementQuantity"])),
                        ft.DataCell(ft.Text(total_cost)),
                        ft.DataCell(
                            ft.Row(
                                controls=
                                    [
                                        EditButton(
                                            on_click_action=lambda e, event_id=budget["EventID"], requirement_name=budget["RequirementName"]: self.edit_budget(event_id, requirement_name)
                                        ),
                                        DeleteButton(
                                            on_click_action=lambda e, event_id=budget["EventID"], requirement_name=budget["RequirementName"]: self.delete_budget(event_id, requirement_name)
                                        ),
                                    ]
                                )
                            ),
                        ]
                    )
                )
        self.page.update()

    def prev_page(self, e):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_display()

    def next_page(self, e):
        total_budgets = self.controller.get_all_budget_list()
        total_pages = (len(total_budgets) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.update_display()

    def on_form_submit(self, form_data, is_edit, original_event_id):
        if is_edit:
            self.controller.edit_budget(
                original_event_id, 
                form_data["RequirementName"], 
                form_data["RequirementBudget"], 
                form_data["RequirementQuantity"]
                )
        else:
            self.controller.add_budget(
                form_data["EventID"], 
                form_data["RequirementName"], 
                form_data["RequirementBudget"], 
                form_data["RequirementQuantity"]
                )
        self.update_display()

    def show_error_dialog(self, message):
        error_dialog = ft.AlertDialog(
            title=ft.Text("Error"),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=lambda e: self.close_error_dialog())]
        )
        self.page.dialog = error_dialog
        error_dialog.open = True
        self.page.update()

    def show_success_dialog(self, message):
        success_dialog = ft.AlertDialog(
            title=ft.Text("Success"),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=lambda e: self.close_success_dialog())]
        )
        self.page.dialog = success_dialog
        success_dialog.open = True
        self.page.update()

    def close_error_dialog(self):
        self.page.dialog.open = False
        self.page.update()

    def close_success_dialog(self):
        self.page.dialog.open = False
        self.page.update()



def main(page: ft.Page):
    app = BudgetManagerApp(page)
    
if __name__ == "__main__":
    ft.app(target=main)