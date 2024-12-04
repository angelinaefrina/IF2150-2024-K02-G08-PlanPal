import tkinter as tk
from tkinter import ttk, messagebox
from guestcontroller import GuestController


class GuestListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Guest List Application")

        # Initialize the controller
        self.controller = GuestController()

        # Frame untuk Treeview (Daftar Tamu)
        self.list_frame = ttk.Frame(root)
        self.list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Treeview untuk menampilkan daftar tamu
        self.tree = ttk.Treeview(self.list_frame, columns=("ID", "Name", "RSVP"), show="headings")
        self.tree.heading("ID", text="Guest ID")
        self.tree.heading("Name", text="Guest Name")
        self.tree.heading("RSVP", text="RSVP Status")
        self.tree.column("ID", width=100)
        self.tree.column("Name", width=200)
        self.tree.column("RSVP", width=150)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Frame untuk tombol aksi
        self.button_frame = ttk.Frame(root)
        self.button_frame.pack(fill=tk.X, padx=10, pady=5)

        # Tombol untuk Add, Edit, Delete
        self.add_button = ttk.Button(self.button_frame, text="Add Guest", command=self.add_guest)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.edit_button = ttk.Button(self.button_frame, text="Edit Guest", command=self.edit_guest)
        self.edit_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = ttk.Button(self.button_frame, text="Delete Guest", command=self.delete_guest)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        # Refresh the treeview
        self.refresh_list()


    def add_guest(self):
        # Form untuk menambahkan tamu baru
        def save_guest():
            # Tambahkan konfirmasi sebelum menambahkan tamu baru
            confirm = messagebox.askyesno("Confirmation", "Are you sure you want to add this guest to the list?")
            if not confirm:
                return
            
            try:
                guest_id = int(entry_id.get().strip())
                guest_name = entry_name.get().strip()
                rsvp_status = rsvp_var.get().strip()

                if not guest_name:
                    raise ValueError("Guest name cannot be empty.")
                if rsvp_status not in ["Accepted", "Declined", "Pending"]:
                    raise ValueError("Invalid RSVP status.")
                
                self.controller.add_guest_list(guest_id, guest_name, rsvp_status)
                self.refresh_list()
                add_window.destroy()
                messagebox.showinfo("Success", "Guest added successfully!")
            except ValueError as e:
                messagebox.showerror("Error", str(e))


        add_window = tk.Toplevel(self.root)
        add_window.title("Add Guest")

        tk.Label(add_window, text="Guest ID:").grid(row=0, column=0, padx=10, pady=5)
        entry_id = tk.Entry(add_window)
        entry_id.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(add_window, text="Guest Name:").grid(row=1, column=0, padx=10, pady=5)
        entry_name = tk.Entry(add_window)
        entry_name.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(add_window, text="RSVP Status:").grid(row=2, column=0, padx=10, pady=5)
        rsvp_var = tk.StringVar(value="Accepted")
        rsvp_dropdown = ttk.Combobox(add_window, textvariable=rsvp_var, values=["Accepted", "Declined", "Pending"])
        rsvp_dropdown.grid(row=2, column=1, padx=10, pady=5)

        save_button = ttk.Button(add_window, text="Save", command=save_guest)
        save_button.grid(row=3, columnspan=2, pady=10)

    def edit_guest(self):
        # Mendapatkan item yang dipilih
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No guest selected.")
            return

        guest = self.tree.item(selected_item, "values")

        def save_changes():

            # Tambahkan konfirmasi sebelum menyimpan perubahan
            confirm = messagebox.askyesno("Confirmation", "Are you sure you want to save these changes?")
            if not confirm:
                return
            try:
                guest_id = int(entry_id.get().strip())
                guest_name = entry_name.get().strip()
                rsvp_status = rsvp_var.get().strip()

                if not guest_name:
                    raise ValueError("Guest name cannot be empty.")
                if rsvp_status not in ["Accepted", "Declined", "Pending"]:
                    raise ValueError("Invalid RSVP status.")

                self.controller.edit_guest_list(int(guest[0]), guest_name, rsvp_status)
                self.refresh_list()
                edit_window.destroy()
                messagebox.showinfo("Success", "Guest updated successfully!")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Guest")

        tk.Label(edit_window, text="Guest ID:").grid(row=0, column=0, padx=10, pady=5)
        entry_id = tk.Entry(edit_window)
        entry_id.insert(0, guest[0])
        entry_id.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(edit_window, text="Guest Name:").grid(row=1, column=0, padx=10, pady=5)
        entry_name = tk.Entry(edit_window)
        entry_name.insert(0, guest[1])
        entry_name.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(edit_window, text="RSVP Status:").grid(row=2, column=0, padx=10, pady=5)
        rsvp_var = tk.StringVar(value=guest[2])
        rsvp_dropdown = ttk.Combobox(edit_window, textvariable=rsvp_var, values=["Accepted", "Declined", "Pending"])
        rsvp_dropdown.grid(row=2, column=1, padx=10, pady=5)

        save_button = ttk.Button(edit_window, text="Save Changes", command=save_changes)
        save_button.grid(row=3, columnspan=2, pady=10)

    def delete_guest(self):
        # Mendapatkan item yang dipilih
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No guest selected.")
            return

        guest = self.tree.item(selected_item, "values")

        # Konfirmasi sebelum menghapus tamu
        confirm = messagebox.askyesno("Confirmation", f"Are you sure you want to delete guest '{guest[1]}'?")
        if not confirm:
            return
        
        self.controller.delete_guest_list(int(guest[0]))
        self.refresh_list()
        messagebox.showinfo("Success", f"Guest with ID {guest[0]} deleted successfully!")

    def refresh_list(self):
        # Bersihkan Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Tambahkan ulang daftar tamu ke Treeview
        for guest in self.controller.guest_list:
            self.tree.insert("", tk.END, values=(guest["GuestID"], guest["GuestName"], guest["RSVPStatus"]))


if __name__ == "__main__":
    root = tk.Tk()
    app = GuestListApp(root)
    root.mainloop()
