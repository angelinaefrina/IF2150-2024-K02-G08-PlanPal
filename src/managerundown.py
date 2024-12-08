from rundown import Rundown
from rundownpage import RundownPage
from rundowncontroller import RundownController
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class ManageRundown(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Manage Rundown")
        self.geometry("800x600")

        # Initialize Controller and Page
        self.rundown_controller = RundownController()
        self.rundown_page = RundownPage(self.rundown_controller)

        self._create_widgets()

    def _create_widgets(self):
        # Input frame
        input_frame = tk.Frame(self)
        input_frame.pack(pady=10, fill=tk.X)

        # Input labels and fields
        tk.Label(input_frame, text="Event ID").grid(row=0, column=0, padx=5, pady=5)
        self.event_id_entry = tk.Entry(input_frame)
        self.event_id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Agenda Name").grid(row=1, column=0, padx=5, pady=5)
        self.agenda_name_entry = tk.Entry(input_frame)
        self.agenda_name_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Start Time").grid(row=0, column=2, padx=5, pady=5)
        self.start_time_entry = tk.Entry(input_frame)
        self.start_time_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(input_frame, text="End Time").grid(row=1, column=2, padx=5, pady=5)
        self.end_time_entry = tk.Entry(input_frame)
        self.end_time_entry.grid(row=1, column=3, padx=5, pady=5)

        # tk.Label(input_frame, text="Duration").grid(row=0, column=4, padx=5, pady=5)
        # self.duration_entry = tk.Entry(input_frame)
        # self.duration_entry.grid(row=0, column=5, padx=5, pady=5)

        tk.Label(input_frame, text="PIC").grid(row=1, column=4, padx=5, pady=5)
        self.pic_entry = tk.Entry(input_frame)
        self.pic_entry.grid(row=1, column=5, padx=5, pady=5)

        # Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Add Rundown", command=self.add_rundown).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Display Rundown", command=self.display_rundown).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Delete Rundown", command=self.delete_rundown).pack(side=tk.LEFT, padx=5)

        # Rundown display area
        self.tree = ttk.Treeview(self, columns=("Event ID", "Agenda Name", "Start Time", "End Time", "Duration", "PIC"), show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True)

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

    def add_rundown(self):
        event_id = self.event_id_entry.get()
        agenda_name = self.agenda_name_entry.get()
        start_time = self.start_time_entry.get()
        end_time = self.end_time_entry.get()
        duration = self.duration_entry.get()
        pic = self.pic_entry.get()

        if not (event_id and agenda_name and start_time and end_time and duration and pic):
            messagebox.showerror("Error", "All fields are required!")
            return

        new_rundown = Rundown(event_id, agenda_name, start_time, end_time, duration, pic)

        if self.rundown_controller.validate_rundown(new_rundown):
            self.rundown_controller.add_rundown(new_rundown)
            self.refresh_treeview()
            messagebox.showinfo("Success", "Rundown added successfully!")

    def delete_rundown(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No rundown selected!")
            return

        values = self.tree.item(selected_item)["values"]
        event_id, agenda_name = values[0], values[1]
        self.rundown_controller.delete_rundown(event_id, agenda_name)
        self.refresh_treeview()
        messagebox.showinfo("Success", f"Rundown '{agenda_name}' deleted successfully!")

    def display_rundown(self):
        event_id = self.event_id_entry.get()
        if not event_id:
            messagebox.showerror("Error", "Event ID is required to display rundown!")
            return

        self.rundown_page.display_rundown(event_id)

    def refresh_treeview(self):
        # Clear treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Add current rundowns
        for rundown in self.rundown_controller.rundown_list:
            self.tree.insert("", tk.END, values=(
                rundown.event_id,
                rundown.agenda_name,
                rundown.agenda_time_start,
                rundown.agenda_time_end,
                rundown.agenda_duration,
                rundown.agenda_pic
            ))


if __name__ == "__main__":
    app = ManageRundown()
    app.mainloop()
