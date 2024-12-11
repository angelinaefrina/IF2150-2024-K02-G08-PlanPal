import flet as ft
from budgetcontroller import ControllerBudget
from budgetform import BudgetForm
from utils.buttons import EditButton, DeleteButton, CreateNewBudget

ITEMS_PER_PAGE = 6

class BudgetManagerApp:
    def __init__(self, page):
        self.page = page
        self.page.title = "Budget Manager"
        
        self.setup_page()

        self.page.bgcolor = ft.colors.with_opacity(1, '#f5e8d9')

        self.controller = ControllerBudget()
        self.budget_form = BudgetForm()

        # data dummy
        self.controller.add_budget(1, "Benda A", 1000, 10)
        self.controller.add_budget(2, "Benda B", 2000, 5)
        self.controller.add_budget(1, "Benda A", 1000, 10)
        self.controller.add_budget(2, "Benda B", 2000, 5)
        self.controller.add_budget(1, "Benda A", 1000, 10)
        self.controller.add_budget(2, "Benda B", 2000, 5)
        self.controller.add_budget(1, "Benda c", 1000, 10)
        self.controller.add_budget(2, "Benda d", 2000, 5)
        self.controller.add_budget(1, "Benda f", 1000, 10)
        self.controller.add_budget(2, "Benda e", 2000, 5)
        self.controller.add_budget(1, "Benda A", 1000, 10)
        self.controller.add_budget(2, "Benda ds", 2000, 5)
        self.controller.add_budget(1, "Benda a", 1000, 10)
        self.controller.add_budget(2, "Benda s", 2000, 5)
        self.controller.add_budget(1, "Benda Aw", 1000, 10)
        self.controller.add_budget(2, "Benda B", 2000, 5)
        self.controller.add_budget(1, "Benda Aa", 1000, 10)
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
            "Header": "assets/fonts/Fredoka/Fredoka-SemiBold.ttf",
            "Default_Bold": "assets/fonts/Afacad/Afacad-Bold.ttf",
            "Default_Regular": "assets/fonts/Afacad/Afacad-Regular.ttf",
        }

        # Add the header (PlanPal text) at the top of the page
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
               # alignment=ft.MainAxisAlignment.CENTER
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
            expand=True
        )
        self.title = ft.Text("Anggaran", size=30, weight=ft.FontWeight.BOLD, color= "#4539B4")
        self.add_button = CreateNewBudget(on_click_action=self.add_budget)
        self.page.add(
        ft.Column(
            controls=[
                self.title,
                self.add_button,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Center horizontally
            )
        )
        self.page.add(ft.Column(
            controls=[
                self.tree,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH)
        )
         # Pagination Controls
        self.page_number_text = ft.Text(f"Page {self.current_page + 1}", size=16, color ="4539B4", weight=ft.FontWeight.BOLD)

        # Pagination Controls
        self.pagination_controls = ft.Row(
            controls=[
                ft.ElevatedButton(text="Previous", color= "#4539B4", bgcolor=ft.colors.LIGHT_BLUE_100, on_click=self.prev_page),
                self.page_number_text,  # Use the pre-declared attribute
                ft.ElevatedButton(text="Next",  color= "#4539B4", bgcolor=ft.colors.LIGHT_BLUE_100, on_click=self.next_page),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
        self.page.add(self.pagination_controls)

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

        all_budgets = self.controller.get_all_budget_list()
        start_index = self.current_page * ITEMS_PER_PAGE
        end_index = start_index + ITEMS_PER_PAGE
        paginated_budgets = all_budgets[start_index:end_index]

        for budget in paginated_budgets:
            total_cost = budget["RequirementBudget"] * budget["RequirementQuantity"]
            self.tree.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(budget["EventID"], color=ft.colors.BLACK87)),
                        ft.DataCell(ft.Text(budget["RequirementName"], color=ft.colors.BLACK87)),
                        ft.DataCell(ft.Text(budget["RequirementBudget"], color=ft.colors.BLACK87)),
                        ft.DataCell(ft.Text(budget["RequirementQuantity"], color=ft.colors.BLACK87)),
                        ft.DataCell(ft.Text(total_cost, color=ft.colors.BLACK87)),
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    EditButton(on_click_action=lambda e, event_id=budget["EventID"], requirement_name=budget["RequirementName"]: self.edit_budget(event_id, requirement_name)),
                                    DeleteButton(on_click_action=lambda e, event_id=budget["EventID"], requirement_name=budget["RequirementName"]: self.delete_budget(event_id, requirement_name)),
                                ]
                            )
                        ),
                    ]
                )
            )

        total_items = len(all_budgets)
        self.pagination_controls.controls[0].disabled = self.current_page == 0  # Disable "Previous" if on first page
        self.pagination_controls.controls[2].disabled = (self.current_page + 1) * ITEMS_PER_PAGE >= total_items  # Disable "Next" if on last page

        self.page_number_text.value = f"Page {self.current_page + 1}"

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

    def prev_page(self, e):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_display()

    def next_page(self, e):
        all_budgets = self.controller.get_all_budget_list()
        if (self.current_page + 1) * ITEMS_PER_PAGE < len(all_budgets):
            self.current_page += 1
            self.update_display()

def main(page: ft.Page):
    app = BudgetManagerApp(page)

ft.app(target=main)