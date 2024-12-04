from budget import Budget
from budgetpage import BudgetPage
from commandbudget import CommandBudget
from controllerbudget import ControllerBudget

class BudgetApplication:
    def __init__(self):
        self.budget_controller = ControllerBudget()

    def display_menu(self):
        print("\n--- Budget Management Application ---")
        print("1. Add Budget")
        print("2. Edit Budget")
        print("3. Delete Budget")
        print("4. Display All Budgets")
        print("5. Exit")

    def add_budget(self):
        try:
            event_id = int(input("Enter Event ID: "))
            requirement_name = input("Enter Requirement Name: ").strip()
            requirement_budget = float(input("Enter Requirement Budget (per unit): "))
            requirement_quantity = int(input("Enter Requirement Quantity: "))
            self.budget_controller.add_budget(event_id, requirement_name, requirement_budget, requirement_quantity)
        except ValueError:
            print("Invalid input. Ensure that Event ID is an integer, Requirement Budget is a number, and Quantity is an integer.")

    def edit_budget(self):
        try:
            event_id = int(input("Enter Event ID to edit: "))
            requirement_name = input("Enter Requirement Name to edit: ").strip()
            new_budget = input("Enter new Requirement Budget (press Enter to skip): ").strip()
            new_quantity = input("Enter new Requirement Quantity (press Enter to skip): ").strip()

            # Convert inputs to appropriate types or set them as None if skipped
            new_budget = float(new_budget) if new_budget else None
            new_quantity = int(new_quantity) if new_quantity else None

            self.budget_controller.edit_budget(event_id, requirement_name, new_budget=new_budget, new_quantity=new_quantity)
        except ValueError:
            print("Invalid input. Ensure the budget and quantity are numeric values.")

    def delete_budget(self):
        try:
            event_id = int(input("Enter Event ID to delete: "))
            requirement_name = input("Enter Requirement Name to delete: ").strip()
            self.budget_controller.delete_budget(event_id, requirement_name)
        except ValueError:
            print("Invalid input. Event ID must be an integer.")

    def display_budgets(self):
        self.budget_controller.display_budget()

    def run(self):
        while True:
            self.display_menu()
            choice = input("Choose an option: ").strip()
            if choice == "1":
                self.add_budget()
            elif choice == "2":
                self.edit_budget()
            elif choice == "3":
                self.delete_budget()
            elif choice == "4":
                self.display_budgets()
            elif choice == "5":
                print("Exiting the application.")
                break
            else:
                print("Invalid choice. Please select a valid option.")


# Run the application
if __name__ == "__main__":
    app = BudgetApplication()
    app.run()

