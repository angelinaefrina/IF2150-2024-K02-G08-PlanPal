class SortEvent:
    def __init__(self, event_list=None):
        self.event_list = event_list if event_list else []

    def display_events_by_status(self, status):
        if not self.event_list:
            print("Tidak ada event yang tersedia.")
            return

        filtered_events = [event for event in self.event_list if event.get_event_status() == status]
        if not filtered_events:
            print(f"Tidak ada event dengan status '{status}'.")
            return

        print(f"Daftar event dengan status '{status}':")
        for event in filtered_events:
            print(f"- Event ID     : {event.get_event_id()}")
            print(f"  Location     : {event.get_event_location()}")
            print(f"  Date         : {event.get_event_date()}")
            print(f"  Status       : {event.get_event_status()}")
            print("-" * 40)

    def sort_events(self, status):
        self.display_events_by_status(status)
