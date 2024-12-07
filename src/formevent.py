import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class FormEvent:
    def __init__(self):
        self.event_details = None

    def display_event_details(self):
        if self.event_details:
            print("Detail Acara:")
            for key, value in self.event_details.items():
                print(f"{key}: {value}")
        else:
            self.display_error_message("Belum ada acara yang tersimpan.")

    # Metode untuk menampilkan form
    # def display_form(self):
        # try:
        #     event_id = input("Masukkan ID acara: ")
        #     event_location = input("Masukkan lokasi acara: ")
        #     event_date = input("Masukkan tanggal acara (YYYY-MM-DD): ")
        #     event_status = input("Masukkan status acara: ")
        #     return {
        #         "EventID": int(event_id),
        #         "EventLocation": event_location,
        #         "EventDate": event_date,
        #         "EventStatus": event_status
        #     }
        # except Exception as e:
        #     self.display_error(f"Error saat mengisi form: {e}")
        #     return None
        ## TKINTER
    def display_form(self, event_data=None):
        self.form_window = tk.Toplevel()
        self.form_window.title("Edit Event")

        tk.Label(self.form_window, text="Event ID:").grid(row=0, column=0)
        self.event_id_entry = tk.Entry(self.form_window)
        self.event_id_entry.grid(row=0, column=1)

        tk.Label(self.form_window, text="Event Location:").grid(row=1, column=0)
        self.event_location_entry = tk.Entry(self.form_window)
        self.event_location_entry.grid(row=1, column=1)

        tk.Label(self.form_window, text="Event Date (YYYY-MM-DD):").grid(row=2, column=0)
        self.event_date_entry = tk.Entry(self.form_window)
        self.event_date_entry.grid(row=2, column=1)

        tk.Label(self.form_window, text="Event Status:").grid(row=3, column=0)
        self.event_status_entry = tk.Entry(self.form_window)
        self.event_status_entry.grid(row=3, column=1)

        if event_data:
            self.event_id_entry.insert(0, event_data["EventID"])
            self.event_location_entry.insert(0, event_data["EventLocation"])
            self.event_date_entry.insert(0, event_data["EventDate"])
            self.event_status_entry.insert(0, event_data["EventStatus"])

        tk.Button(self.form_window, text="Submit", command=self.submit_form).grid(row=4, column=0, columnspan=2)

    # Metode untuk menyimpan form detail acara
    # def submit_form(self, form_data):
    #     if form_data and self.validate_form_data(form_data):
    #         self.event_details = form_data
    #         print("Detail acara berhasil disimpan!")
    #     else:
    #         self.display_error_message("Data form tidak valid.")
    ## TKINTER
    def submit_form(self):
        form_data = {
            "EventID": int(self.event_id_entry.get()),
            "EventLocation": self.event_location_entry.get(),
            "EventDate": self.event_date_entry.get(),
            "EventStatus": self.event_status_entry.get()
        }
        if self.validate_form_data(form_data):
            self.event_details = form_data
            self.form_window.destroy()
            print("Detail acara berhasil disimpan!")
        else:
            self.display_error_message("Data form tidak valid.")

    def display_error_message(self, message):
        print(f"Error: {message}")

    # Metode untuk menampilkan pesan error jika data invalid
    def display_error(self, error_message):
        print(f"Error: {error_message}")

    # Metode tambahan untuk validasi data form
    def validate_form_data(self, form_data):
        required_fields = ["EventID", "EventLocation", "EventDate", "EventStatus"]
        for field in required_fields:
            if field not in form_data or not form_data[field]:
                self.display_error_message(f"Field '{field}' tidak boleh kosong.")
                return False
        return True