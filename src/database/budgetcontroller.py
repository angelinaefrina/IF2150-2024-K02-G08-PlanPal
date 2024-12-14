class ControllerBudget:
    def __init__(self):
        self.budget_database = []

    def add_budget(self, event_id, requirement_name, requirement_budget, requirement_quantity):
        if self.validate_budget(requirement_budget, requirement_quantity):
            new_budget = {
                "EventID": event_id,
                "RequirementName": requirement_name,
                "RequirementBudget": requirement_budget,
                "RequirementQuantity": requirement_quantity
            }
            self.budget_database.append(new_budget)
            print(f"Anggaran untuk event {event_id} berhasil ditambahkan.")
        else:
            print("Data anggaran tidak valid. Penambahan dibatalkan.")

    def edit_budget(self, original_event_id, requirement_name, requirement_budget, requirement_quantity):
        # Find the budget entry to update
        for budget in self.budget_database:
            if budget["EventID"] == original_event_id:
                budget["RequirementName"] = requirement_name
                budget["RequirementBudget"] = requirement_budget
                budget["RequirementQuantity"] = requirement_quantity
                print(f"Updated budget: {budget}")
                break
    
    def delete_budget(self, event_id, requirement_name):
        for budget in self.budget_database:
            if budget["EventID"] == event_id and budget["RequirementName"] == requirement_name:
                self.budget_database.remove(budget)
                print(f"Anggaran untuk {requirement_name} pada event {event_id} berhasil dihapus.")
                return
        print(f"Anggaran untuk {requirement_name} pada event {event_id} tidak ditemukan.")

    def validate_budget(self, requirement_budget, requirement_quantity):
        if requirement_budget < 0:
            print("Anggaran tidak boleh bernilai negatif.")
            return False
        if requirement_quantity <= 0:
            print("Kuantitas harus lebih besar dari 0.")
            return False
        return True

    def display_budget(self):
        if not self.budget_database:
            print("Database anggaran kosong.")
            return

        print("Database Anggaran:")
        for budget in self.budget_database:
            total_cost = budget["RequirementBudget"] * budget["RequirementQuantity"]
            print(
                f"- EventID: {budget['EventID']}, "
                f"Requirement: {budget['RequirementName']}, "
                f"Budget per Unit: {budget['RequirementBudget']}, "
                f"Quantity: {budget['RequirementQuantity']}, "
                f"Total Cost: {total_cost}"
            )
        
    def get_all_budget_list(self):
        return self.budget_database

    def get_budget_list(self, event_id):
        budgets = [budget for budget in self.budget_database if budget["EventID"] == event_id]
        if budgets:
            return budgets
        else:
            print(f"No budgets found for EventID {event_id}.")
            return []
        
'''
    def edit_budget(self, event_id, requirement_name, new_budget=None, new_quantity=None):
        for budget in self.budget_database:
            if budget["EventID"] == event_id and budget["RequirementName"] == requirement_name:
                if new_budget is not None:
                    if new_budget < 0:
                        print("Anggaran tidak boleh bernilai negatif. Perubahan dibatalkan.")
                        return
                    budget["RequirementBudget"] = new_budget
                if new_quantity is not None:
                    if new_quantity <= 0:
                        print("Kuantitas harus lebih besar dari 0. Perubahan dibatalkan.")
                        return
                    budget["RequirementQuantity"] = new_quantity
                print(f"Anggaran untuk {requirement_name} pada event {event_id} berhasil diperbarui.")
                return
        print(f"Anggaran untuk {requirement_name} pada event {event_id} tidak ditemukan.")
'''
