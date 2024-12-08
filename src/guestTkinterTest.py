import tkinter as tk
from tkinter import ttk, messagebox, font
from guestcontroller import GuestController


class GuestListApp:
    def __init__(self, root):



        self.root = root
        self.root.title("PlanPal - Daftar Tamu")
        self.root.configure(bg="#FDF6E3")  # Background krem

        # Custom font
        self.title_font = font.Font(family="Helvetica", size=24, weight="bold")
        self.button_font = font.Font(family="Helvetica", size=12)

        # Judul
        tk.Label(self.root, text="PlanPal", font=self.title_font, bg="#FDF6E3", fg="#4A90E2").pack(pady=10)
        tk.Label(self.root, text="Daftar Tamu", font=self.title_font, bg="#FDF6E3").pack(pady=5)

        # Initialize the controller
        self.controller = GuestController()

        # Frame untuk Treeview
        self.list_frame = tk.Frame(root, bg="#FDF6E3")
        self.list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.tree = ttk.Treeview(self.list_frame, columns=("ID", "Name", "RSVP"), show="headings", height=10)
        self.tree.heading("ID", text="Nama")
        self.tree.heading("Name", text="Status")
        self.tree.column("ID", anchor="center", width=200)
        self.tree.column("Name", anchor="center", width=150)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

        # Frame untuk tombol
        self.button_frame = tk.Frame(root, bg="#FDF6E3")
        self.button_frame.pack(fill=tk.X, pady=5)
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

        self.add_button = ttk.Button(self.button_frame, text="Tambah", bg="#ADD8E6", fg="#000", font=self.button_font, command=self.add_guest)
        self.add_button.pack(side=tk.LEFT, padx=10)

        self.edit_button = ttk.Button(self.button_frame, text="Edit", bg="#ADD8E6", fg="#000", font=self.button_font, command=self.edit_guest)
        self.edit_button.pack(side=tk.LEFT, padx=10)

        self.delete_button = ttk.Button(self.button_frame, text="Hapus", bg="#ADD8E6", fg="#000", font=self.button_font, command=self.delete_guest)
        self.delete_button.pack(side=tk.LEFT, padx=10)

        self.refresh_list()

    def refresh_list(self):
        """Refresh the Treeview to display the updated guest list."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        for guest in self.controller.guest_list:
            self.tree.insert("", "end", values=(guest["GuestID"], guest["GuestName"], guest["RSVPStatus"]))

    def add_guest(self):
        """Add a new guest using a popup form."""
        def save_guest():
            guest_name = entry_name.get().strip()
            rsvp_status = rsvp_var.get().strip()

            try:
                # Generate Guest ID otomatis
                if self.controller.guest_list:
                    guest_id = max(guest["GuestID"] for guest in self.controller.guest_list) + 1
                else:
                    guest_id = 1

                self.controller.add_guest_list(guest_id, guest_name, rsvp_status)
                self.refresh_list()
                add_window.destroy()
                messagebox.showinfo("Success", "Guest added successfully!")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        add_window = tk.Toplevel(self.root)
        add_window.title("Add Guest")

        tk.Label(add_window, text="Guest Name:").grid(row=0, column=0, padx=10, pady=5)
        entry_name = tk.Entry(add_window)
        entry_name.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(add_window, text="RSVP Status:").grid(row=1, column=0, padx=10, pady=5)
        rsvp_var = tk.StringVar(value="Hadir")
        rsvp_dropdown = ttk.Combobox(add_window, textvariable=rsvp_var, values=["Hadir", "Tidak Hadir", "Menyusul"], state="readonly")
        rsvp_dropdown.grid(row=1, column=1, padx=10, pady=5)

        save_button = ttk.Button(add_window, text="Save", command=save_guest)
        save_button.grid(row=2, columnspan=2, pady=10)

    def edit_guest(self):
        """Edit an existing guest."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No guest selected.")
            return

        guest = self.tree.item(selected_item, "values")

        def save_changes():
            guest_name = entry_name.get().strip()
            rsvp_status = rsvp_var.get().strip()

            try:
                self.controller.edit_guest_list(int(guest[0]), guest_name, rsvp_status)
                self.refresh_list()
                edit_window.destroy()
                messagebox.showinfo("Success", "Guest updated successfully!")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Guest")

        tk.Label(edit_window, text="Guest Name:").grid(row=0, column=0, padx=10, pady=5)
        entry_name = tk.Entry(edit_window)
        entry_name.insert(0, guest[1])
        entry_name.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(edit_window, text="RSVP Status:").grid(row=1, column=0, padx=10, pady=5)
        rsvp_var = tk.StringVar(value=guest[2])
        rsvp_dropdown = ttk.Combobox(edit_window, textvariable=rsvp_var, values=["Hadir", "Tidak Hadir", "Menyusul"], state="readonly")
        rsvp_dropdown.grid(row=1, column=1, padx=10, pady=5)

        save_button = ttk.Button(edit_window, text="Save", command=save_changes)
        save_button.grid(row=2, columnspan=2, pady=10)

    def delete_guest(self):
        # Mendapatkan item yang dipilih
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No guest selected.")
            return

        # Ambil data tamu dari item yang dipilih
        guest = self.tree.item(selected_item, "values")
        guest_id = int(guest[0])  # Guest ID ada di kolom pertama

        # Konfirmasi sebelum menghapus
        confirm = messagebox.askyesno("Confirmation", f"Are you sure you want to delete guest with ID {guest_id}?")
        if not confirm:
            return

        try:
            # Hapus tamu dari GuestController
            self.controller.delete_guest_list(guest_id)

            # Refresh tampilan daftar tamu
            self.refresh_list()

            # Berikan pesan sukses
            messagebox.showinfo("Success", f"Guest with ID {guest_id} has been deleted.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = GuestListApp(root)
    root.mainloop()
