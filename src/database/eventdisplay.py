class EventDisplay:
    def __init__(self, event_list=None):
        self.event_list = event_list if event_list else []

    def display_event_list(self, filtered_list=None):
        if not self.event_list:
            self.display_error("Tidak ada event yang tersedia.")
            return
        print("Daftar Event:")
        events = self.controller_event.get_all_events()
        for event in events:
            print(f"Event ID: {event.event_id}, Lokasi: {event.event_location}, Tanggal: {event.event_date}, Status: {event.event_status}")

    def display_error(self, error_message):
        print(f"Error: {error_message}")

    def display_sort_options(self):
        print("Pilih status acara:")
        print("Belum dimulai")
        print("Sedang berlangsung")
        print("Sudah selesai")
        print("Batal")

    def sort_event_list(self, criteria):
        if criteria in ['EventStatus']:
            self.event_list.sort(key=lambda x: x[criteria])
            print(f"Daftar event yang memiliki status '{criteria}'.")
        else:
            self.display_error("Kriteria pengurutan tidak valid.")

    def filter_event_list(self, status):
        filtered_list = [event for event in self.event_list if event["EventStatus"] == status]
        if not filtered_list:
            print(f"Tidak ada event dengan status '{status}'.")
        else:
            print(f"Daftar event dengan status '{status}':")
            self.display_event_list(filtered_list)