from .database import EventDatabase

class ControllerEvent:
    def __init__(self, event_db):
        # self._event_list = []
        self.event_db = event_db
        self.events = self.load_events()

    # Metode untuk mengambil daftar event
    def get_event_list(self):
        return self.event_db.get_all_events()

    def load_events(self):
        return self.event_db.get_all_events()

    # Metode untuk mengambil detail event spesifik
    def get_event_details(self, event_id):
        # for event in self._event_list:
        #     if event['EventID'] == event_id:
        #         return event
        # return None
        for event in self.events:
            if event[0] == event_id:
                return {
                    "EventID": event[0],
                    "EventName": event[1],
                    "EventLocation": event[2],
                    "EventDate": event[3],
                    "EventStatus": event[4]
                }
        return None

    def validate_event_list(self):
        return len(self._event_list) > 0

    def add_event(self, event_id, event_name, event_location, event_date, event_status):
        # new_event = {
        #     "EventID": event_id,
        #     "EventName": eventname,
        #     "EventLocation": location,
        #     "EventDate": date,
        #     "EventStatus": status
        # }
        self.event_db.add_event(event_id, event_name, event_location, event_date, event_status)
        self.events = self.load_events()

    # Metode untuk mengedit data event
    def edit_event(self, event_id, **kwargs):
        for event in self._event_list:
            if event['EventID'] == event_id:
                event.update(kwargs)
                return True
        return False

    def delete_event(self, event_id):
        # for event in self._event_list:
        #     if event['EventID'] == event_id:
        #         self._event_list.remove(event)
        #         return True
        # return False
        query = "DELETE FROM Event WHERE EventID = ?"
        self.event_db.execute_query(query, (event_id,))
        self.events = self.load_events()

    def sort_event_list(self, criteria):
        self._event_list.sort(key=lambda x: x[criteria])
        return True
