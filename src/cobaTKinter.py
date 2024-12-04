import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from controllerbudget import ControllerBudget

class BudgetAppTkinter:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Management Application")
        self.controller = ControllerBudget()

        # Title Label
        title = tk.Label(root, text="Budget Management Application", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        # Frame for Buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Add Budget", command=self.open_add_budget_window).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Edit Budget", command=self.open_edit_budget_window).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Delete Budget", command=self.open_delete_budget_window).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Refresh", command=self.display_budgets).grid(row=0, column=3, padx=5)

        # Treeview for Budget Display
        self.tree = ttk.Treeview(root, columns=("EventID", "Requirement", "Budget", "Quantity", "Total"), show="headings")
        self.tree.heading("EventID", text="Event ID")
        self.tree.heading("Requirement", text="Requirement")
        self.tree.heading("Budget", text="Budget/Unit")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Total", text="Total Cost")
        self.tree.pack(pady=10, fill="both", expand=True)

        self.display_budgets()

    def display_budgets(self):
        # Clear existing rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Add rows to the treeview
        for budget in self.controller.budget_database:
            total_cost = budget["RequirementBudget"] * budget["RequirementQuantity"]
            self.tree.insert("", "end", values=(
                budget["EventID"],
                budget["RequirementName"],
                budget["RequirementBudget"],
                budget["RequirementQuantity"],
                total_cost
            ))

    def open_add_budget_window(self):
        window = tk.Toplevel(self.root)
        window.title("Add Budget")

        tk.Label(window, text="Event ID:").grid(row=0, column=0, padx=5, pady=5)
        event_id_entry = tk.Entry(window)
        event_id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(window, text="Requirement Name:").grid(row=1, column=0, padx=5, pady=5)
        req_name_entry = tk.Entry(window)
        req_name_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(window, text="Requirement Budget:").grid(row=2, column=0, padx=5, pady=5)
        budget_entry = tk.Entry(window)
        budget_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(window, text="Requirement Quantity:").grid(row=3, column=0, padx=5, pady=5)
        quantity_entry = tk.Entry(window)
        quantity_entry.grid(row=3, column=1, padx=5, pady=5)

        def add_budget():
            try:
                event_id = int(event_id_entry.get())
                req_name = req_name_entry.get().strip()
                budget = float(budget_entry.get())
                quantity = int(quantity_entry.get())
                self.controller.add_budget(event_id, req_name, budget, quantity)
                messagebox.showinfo("Success", "Budget added successfully!")
                self.display_budgets()
                window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please check your entries.")

        tk.Button(window, text="Add", command=add_budget).grid(row=4, column=0, columnspan=2, pady=10)

    def open_edit_budget_window(self):
        window = tk.Toplevel(self.root)
        window.title("Edit Budget")

        tk.Label(window, text="Event ID:").grid(row=0, column=0, padx=5, pady=5)
        event_id_entry = tk.Entry(window)
        event_id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(window, text="Requirement Name:").grid(row=1, column=0, padx=5, pady=5)
        req_name_entry = tk.Entry(window)
        req_name_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(window, text="New Requirement Budget:").grid(row=2, column=0, padx=5, pady=5)
        budget_entry = tk.Entry(window)
        budget_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(window, text="New Requirement Quantity:").grid(row=3, column=0, padx=5, pady=5)
        quantity_entry = tk.Entry(window)
        quantity_entry.grid(row=3, column=1, padx=5, pady=5)

        def edit_budget():
            try:
                event_id = int(event_id_entry.get())
                req_name = req_name_entry.get().strip()
                new_budget = float(budget_entry.get()) if budget_entry.get() else None
                new_quantity = int(quantity_entry.get()) if quantity_entry.get() else None
                self.controller.edit_budget(event_id, req_name, new_budget, new_quantity)
                messagebox.showinfo("Success", "Budget edited successfully!")
                self.display_budgets()
                window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please check your entries.")

        tk.Button(window, text="Edit", command=edit_budget).grid(row=4, column=0, columnspan=2, pady=10)

    def open_delete_budget_window(self):
        window = tk.Toplevel(self.root)
        window.title("Delete Budget")

        tk.Label(window, text="Event ID:").grid(row=0, column=0, padx=5, pady=5)
        event_id_entry = tk.Entry(window)
        event_id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(window, text="Requirement Name:").grid(row=1, column=0, padx=5, pady=5)
        req_name_entry = tk.Entry(window)
        req_name_entry.grid(row=1, column=1, padx=5, pady=5)

        def delete_budget():
            try:
                event_id = int(event_id_entry.get())
                req_name = req_name_entry.get().strip()
                self.controller.delete_budget(event_id, req_name)
                messagebox.showinfo("Success", "Budget deleted successfully!")
                self.display_budgets()
                window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please check your entries.")

        tk.Button(window, text="Delete", command=delete_budget).grid(row=2, column=0, columnspan=2, pady=10)


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetAppTkinter(root)
    root.mainloop()
