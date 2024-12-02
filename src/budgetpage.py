class BudgetPage:
    def __init__(self, controller_budget):
        self.controller_budget = controller_budget

    def display_budget(self, event_id):
        print(f"=== Anggaran untuk EventID {event_id} ===")
        event_budgets = [
            budget for budget in self.controller_budget.budget_database
            if budget["EventID"] == event_id
        ]

        if not event_budgets:
            print(f"Tidak ada anggaran yang ditemukan untuk EventID {event_id}.")
            return

        for budget in event_budgets:
            total_cost = budget["RequirementBudget"] * budget["RequirementQuantity"]
            print(
                f"- Requirement: {budget['RequirementName']}, "
                f"Budget per Unit: {budget['RequirementBudget']}, "
                f"Quantity: {budget['RequirementQuantity']}, "
                f"Total Cost: {total_cost}"
            )
        print("=============================")

    def display_edit_budget(self, event_id):
        print(f"=== Edit Anggaran untuk EventID {event_id} ===")
        requirement_name = input("Masukkan nama kebutuhan yang ingin diubah: ")
        
        # Mencari anggaran yang cocok
        budget_found = next(
            (budget for budget in self.controller_budget.budget_database
             if budget["EventID"] == event_id and budget["RequirementName"] == requirement_name),
            None
        )

        if not budget_found:
            print(f"Tidak ada anggaran untuk '{requirement_name}' pada EventID {event_id}.")
            return

        print("Detail Anggaran Saat Ini:")
        print(f"- Requirement: {budget_found['RequirementName']}")
        print(f"- Budget per Unit: {budget_found['RequirementBudget']}")
        print(f"- Quantity: {budget_found['RequirementQuantity']}")
        
        # Input perubahan
        try:
            new_budget = int(input("Masukkan anggaran baru per unit (tekan Enter untuk melewati): ") or budget_found["RequirementBudget"])
            new_quantity = int(input("Masukkan jumlah baru (tekan Enter untuk melewati): ") or budget_found["RequirementQuantity"])
            
            # Memperbarui anggaran
            self.controller_budget.edit_budget(event_id, requirement_name, new_budget=new_budget, new_quantity=new_quantity)
        except ValueError:
            print("Input tidak valid. Pastikan memasukkan angka untuk anggaran dan jumlah.")