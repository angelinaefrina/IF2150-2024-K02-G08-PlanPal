# from event import Event
# from eventdisplay import EventDisplay
# from formevent import FormEvent
# from controllerevent import ControllerEvent

# # Create instances of the classes
# controller = ControllerEvent()
# event_display = EventDisplay(controller.get_event_list())

# # Add some events
# controller.add_event("1", "Location A", "2023-10-01", "Belum dimulai")
# controller.add_event("2", "Location B", "2023-10-02", "Sedang berlangsung")
# controller.add_event("3", "Location C", "2023-10-03", "Sudah selesai")
# event_display.event_list = controller.get_event_list()
# # Update the event list in EventDisplay
# # event_display.event_list = controller.get_event_list()

# # Display the event list
# # event_display.display_event_list()

# # Display sort options
# # event_display.display_sort_options()

# while True:
#     user_input = input(">>> ")
#     if user_input.upper() == "LIST":
#         event_display.display_event_list()
#     elif user_input.upper() == "ADD":
#         form_event = FormEvent()
#         form_data = form_event.display_form()
#         form_event.submit_form(form_data)
#         event_data = form_data
#         controller.add_event(event_data["EventID"], event_data["EventLocation"], event_data["EventDate"], event_data["EventStatus"])
#         event_display.event_list = controller.get_event_list()
#         event_display.display_event_list()
#     elif user_input.upper() == "EDIT":
#         event_id = input("Masukkan ID acara yang ingin diedit: ")
#         if controller.get_event_details(event_id) is None:
#             print(f"Error: Event dengan ID '{event_id}' tidak ditemukan.")
#         else:
#             form_event = FormEvent()
#             form_data = form_event.display_form()
#             form_event.submit_form(form_data)
#             if form_event.event_details:
#                 controller.edit_event(event_id, **form_event.event_details)
#                 event_display.event_list = controller.get_event_list()
#                 event_display.display_event_list()
#     elif user_input.upper() == "HAPUS":
#         event_id = input("Masukkan ID acara yang ingin dihapus: ")
#         if controller.get_event_details(event_id) is None:
#             print(f"Error: Event dengan ID '{event_id}' tidak ditemukan.")
#         else:
#             controller.delete_event(event_id)
#             event_display.event_list = controller.get_event_list()
#             event_display.display_event_list()
#     elif user_input.upper() == "EXIT":
#         break

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from event import Event
from eventdisplay import EventDisplay
from formevent import FormEvent
from controllerevent import ControllerEvent

class EventManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Event Manager")
        
        self.controller = ControllerEvent()
        self.event_display = EventDisplay(self.controller.get_event_list())
        self.form_event = FormEvent()
        
        self.controller.add_event(1, "Location A", "2023-10-01", "Belum dimulai")
        self.controller.add_event(2, "Location B", "2023-10-02", "Sedang berlangsung")
        self.controller.add_event(3, "Location C", "2023-10-03", "Sudah selesai")
        self.event_display.event_list = self.controller.get_event_list()
        
        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        self.tree = ttk.Treeview(self.root, columns=("EventID", "Location", "Date", "Status"), show='headings')
        self.tree.heading("EventID", text="Event ID", anchor=tk.CENTER)
        self.tree.heading("Location", text="Location", anchor=tk.CENTER)
        self.tree.heading("Date", text="Date", anchor=tk.CENTER)
        self.tree.heading("Status", text="Status", anchor=tk.CENTER)

        self.tree.column("EventID", anchor=tk.CENTER)
        self.tree.column("Location", anchor=tk.CENTER)
        self.tree.column("Date", anchor=tk.CENTER)
        self.tree.column("Status", anchor=tk.CENTER)

        self.tree.pack(expand=True, fill='both')

        self.add_button = tk.Button(self.root, text="Add Event", command=self.add_event)
        self.add_button.pack()

        self.edit_button = tk.Button(self.root, text="Edit Event", command=self.edit_event)
        self.edit_button.pack()

        self.delete_button = tk.Button(self.root, text="Delete Event", command=self.delete_event)
        self.delete_button.pack()

        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.quit)
        self.exit_button.pack()

    # def add_event(self):
    #     form_data = self.form_event.display_form()
    #     self.form_event.submit_form(form_data)
    #     if self.form_event.event_details:
    #         self.controller.add_event(
    #             self.form_event.event_details["EventID"],
    #             self.form_event.event_details["EventLocation"],
    #             self.form_event.event_details["EventDate"],
    #             self.form_event.event_details["EventStatus"]
    #         )
    #         self.update_display()

    def add_event(self):
        self.form_event.display_form()
        self.root.wait_window(self.form_event.form_window)  # Wait for the form window to close
        if self.form_event.event_details:
            self.controller.add_event(
                self.form_event.event_details["EventID"],
                self.form_event.event_details["EventLocation"],
                self.form_event.event_details["EventDate"],
                self.form_event.event_details["EventStatus"]
            )
            self.update_display()

    def edit_event(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            event_id = item["values"][0]
            
            if self.controller.get_event_details(event_id) is None:
                messagebox.showerror("Error", f"Event with ID '{event_id}' not found.")
            else:
                event_data = self.controller.get_event_details(event_id)
                self.form_event.display_form(event_data)
                self.root.wait_window(self.form_event.form_window)  # Wait for the form window to close
                if self.form_event.event_details:
                    self.controller.edit_event(event_id, **self.form_event.event_details)
                    self.update_display()
        else:
            messagebox.showwarning("Warning", "No event selected.")

    def delete_event(self):
        selected_item = self.tree.selection()
        if selected_item:
            event_id = self.tree.item(selected_item)["values"][0]
            if self.controller.get_event_details(event_id) is None:
                messagebox.showerror("Error", f"Event with ID '{event_id}' not found.")
            else:
                self.controller.delete_event(event_id)
                self.update_display()
        else:
            messagebox.showwarning("Warning", "No event selected.")

    def update_display(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for event in self.event_display.event_list:
            self.tree.insert("", tk.END, values=(event["EventID"], event["EventLocation"], event["EventDate"], event["EventStatus"]))

if __name__ == "__main__":
    root = tk.Tk()
    app = EventManagerApp(root)
    root.mainloop()