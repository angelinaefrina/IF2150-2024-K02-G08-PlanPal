class ControllerBudget:
    def __init__(self, budget_db):
        self.budget_db = budget_db

    def add_budget(self, event_id, requirement_name, requirement_budget, requirement_quantity):
        budget_data = {
            "EventID": event_id,
            "RequirementName": requirement_name,
            "RequirementBudget": requirement_budget,
            "RequirementQuantity": requirement_quantity
        }
        if self.validate_budget_data(budget_data):
            self.budget_db.add_budget(event_id, requirement_name, requirement_budget, requirement_quantity)            
            print(f"budget '{requirement_name}' berhasil ditambahkan untuk EventID {event_id}.")
        else:
            print("Gagal menambahkan budget. Data tidak valid.")
    
    def validate_budget_data(self, budget_data):
        required_fields = ["EventID", "RequirementName", "RequirementBudget", "RequirementQuantity"]
        for field in required_fields:
            if field not in budget_data or not budget_data[field]:
                print(f"Validasi gagal: '{field}' harus diisi.")
                return False

        return True

    # def edit_budget(self, original_event_id, requirement_name, requirement_budget, requirement_quantity):
    #     # Find the budget entry to update
    #     for budget in self.budget_database:
    #         if budget["EventID"] == original_event_id:
    #             budget["RequirementName"] = requirement_name
    #             budget["RequirementBudget"] = requirement_budget
    #             budget["RequirementQuantity"] = requirement_quantity
    #             print(f"Updated budget: {budget}")
    #             break
        
    def edit_budget(self, original_event_id, requirement_name, requirement_budget, requirement_quantity):
        budget_data = {
            "EventID": original_event_id,
            "RequirementName": requirement_name,
            "RequirementBudget": requirement_budget,
            "RequirementQuantity": requirement_quantity
        }
        if self.validate_budget_data(budget_data):
            # self.vendor_db.update_vendor(vendor_data)
            self.budget_db.delete_budget(original_event_id, requirement_name)
            self.budget_db.add_budget(original_event_id, requirement_name, requirement_budget, requirement_quantity)
            print(f"Vendor '{requirement_name}' berhasil diperbarui untuk EventID {original_event_id}.")
        else:
            print("Gagal memperbarui vendor. Data tidak valid.")


    
    def delete_budget(self, event_id, requirement_name):
        if self.budget_db.delete_budget(event_id, requirement_name):
            print(f"Budget '{requirement_name}' berhasil dihapus dari EventID {event_id}.")
        else:
            print(f"Budget '{requirement_name}' tidak ditemukan untuk EventID {event_id}.")

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
        
    # def get_all_budget_list(self):
    #     budgets = self.budget_db.select_all_budgets()

    #     if not budgets:
    #         print(f"Tidak ada budget yang ditemukan.")
    #     return budgets
    
    def get_budget_list(self, event_id):
        budgets = self.budget_db.get_budget_list(event_id)
        if not budgets:
            print(f"Tidak ada vendor yang ditemukan untuk EventID {event_id}.")
        return budgets
        
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
