class ControllerEvent:
    def __init__(self):
        self._event_list = []

    # Metode untuk mengambil daftar event
    def get_event_list(self):
        return self._event_list

    # Metode untuk mengambil detail event spesifik
    def get_event_details(self, event_id):
        for event in self._event_list:
            if event['EventID'] == event_id:
                return event
        return None

    def validate_event_list(self):
        return len(self._event_list) > 0

    def add_event(self, event_id, location, date, status):
        new_event = {
            "EventID": event_id,
            "EventLocation": location,
            "EventDate": date,
            "EventStatus": status
        }
        self._event_list.append(new_event)

    # Metode untuk mengedit data event
    def edit_event(self, event_id, **kwargs):
        for event in self._event_list:
            if event['EventID'] == event_id:
                event.update(kwargs)
                return True
        return False

    def delete_event(self, event_id):
        for event in self._event_list:
            if event['EventID'] == event_id:
                self._event_list.remove(event)
                return True
        return False

    def sort_event_list(self, criteria):
        self._event_list.sort(key=lambda x: x[criteria])
        return True
