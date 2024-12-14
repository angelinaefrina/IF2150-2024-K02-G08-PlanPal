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

    def submit_form(self):
        event_id, event_location, event_date, event_status = self.display_form()
        self.controller_event.add_event(event_id, event_location, event_date, event_status)

    def display_error_message(self, message):
        print(f"Error: {message}")

    def display_error(self, error_message):
        print(f"Error: {error_message}")

    def validate_form_data(self, form_data):
        required_fields = ["EventID", "EventLocation", "EventDate", "EventStatus"]
        for field in required_fields:
            if field not in form_data or not form_data[field]:
                self.display_error_message(f"Field '{field}' tidak boleh kosong.")
                return False
        return True