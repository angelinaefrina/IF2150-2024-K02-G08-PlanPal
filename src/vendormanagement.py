import tkinter as tk
from tkinter import messagebox
from database import add_vendor, update_vendor, delete_vendor, get_vendor_by_event, get_all_vendors

class VendorManagement:
    def __init__(self, root):
        self.root = root
        self.root.title("Vendor Management")
        self.create_widgets()

    def create_widgets(self):
        self.event_id_label = tk.Label(self.root, text="Event ID")
        self.event_id_label.grid(row=0, column=0)
        self.event_id_entry = tk.Entry(self.root)
        self.event_id_entry.grid(row=0, column=1)
        self.vendor_name_label = tk.Label(self.root, text="Vendor Name")
        self.vendor_name_label.grid(row=1, column=0)
        self.vendor_name_entry = tk.Entry(self.root)
        self.vendor_name_entry.grid(row=1, column=1)
        self.vendor_contact_label = tk.Label(self.root, text="Vendor Contact")
        self.vendor_contact_label.grid(row=2, column=0)
        self.vendor_contact_entry = tk.Entry(self.root)
        self.vendor_contact_entry.grid(row=2, column=1)
        self.vendor_product_label = tk.Label(self.root, text="Vendor Product")
        self.vendor_product_label.grid(row=3, column=0)
        self.vendor_product_entry = tk.Entry(self.root)
        self.vendor_product_entry.grid(row=3, column=1)
        self.add_button = tk.Button(self.root, text="Add Vendor", command=self.add_vendor)
        self.add_button.grid(row=4, column=0)
        self.update_button = tk.Button(self.root, text="Update Vendor", command=self.update_vendor)
        self.update_button.grid(row=4, column=1)
        self.delete_button = tk.Button(self.root, text="Delete Vendor", command=self.delete_vendor)
        self.delete_button.grid(row=5, column=0)
        self.view_button = tk.Button(self.root, text="View Vendor", command=self.view_vendor)
        self.view_button.grid(row=5, column=1)
        self.vendor_listbox = tk.Listbox(self.root, width=50, height=10)
        self.vendor_listbox.grid(row=6, column=0, columnspan=2)
        self.load()

    def load(self):
        self.vendor_listbox.delete(0, tk.END)
        vendors = get_all_vendors()
        for vendor in vendors:
            display_text = f"Event ID: {vendor[0]}, Name: {vendor[1]}, Contact: {vendor[2]}, Product: {vendor[3]}"
            self.vendor_listbox.insert(tk.END, display_text)

    def tambah(self):
        try:
            event_id = int(self.event_id_entry.get())
            vendor_name = self.vendor_name_entry.get()
            vendor_contact = self.vendor_contact_entry.get()
            vendor_product = self.vendor_product_entry.get()
            add_vendor(event_id, vendor_name, vendor_contact, vendor_product)
            messagebox.showinfo("Success", "Vendor added successfully")
            self.load_vendor_list()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add vendor: {e}")

    def edit(self):
        try:
            event_id = int(self.event_id_entry.get())
            vendor_name = self.vendor_name_entry.get()
            vendor_contact = self.vendor_contact_entry.get()
            vendor_product = self.vendor_product_entry.get()
            update_vendor(event_id, vendor_name, vendor_contact, vendor_product)
            messagebox.showinfo("Success", "Vendor updated successfully")
            self.load_vendor_list()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update vendor: {e}")

    def hapus(self):
        try:
            event_id = int(self.event_id_entry.get())
            delete_vendor(event_id)
            messagebox.showinfo("Success", "Vendor deleted successfully")
            self.load_vendor_list()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete vendor: {e}")

    def lihat(self):
        try:
            event_id = int(self.event_id_entry.get())
            vendor = get_vendor_by_event(event_id)
            if vendor:
                self.vendor_name_entry.delete(0, tk.END)
                self.vendor_name_entry.insert(0, vendor[1])
                self.vendor_contact_entry.delete(0, tk.END)
                self.vendor_contact_entry.insert(0, vendor[2])
                self.vendor_product_entry.delete(0, tk.END)
                self.vendor_product_entry.insert(0, vendor[3])
            else:
                messagebox.showinfo("Data Kosong", "Vendor belum ditambahkan")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to view vendor: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VendorManagementApp(root)
    root.mainloop()
