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
    def display_form(self):
        try:
            event_id = input()
            event_location = input()
            event_date = input()
            event_status = input()
            return {
                "EventID": event_id,
                "EventLocation": event_location,
                "EventDate": event_date,
                "EventStatus": event_status
            }
        except Exception as e:
            self.display_error(f"Error saat mengisi form: {e}")
            return None

    # Metode untuk menyimpan form detail acara
    def submit_form(self, form_data):
        if form_data and self.validate_form_data(form_data):
            self.event_details = form_data
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