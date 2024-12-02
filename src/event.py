class Event:
    def __init__(self, event_id=None, event_location=None, event_date=None, event_status=None):
        self._event_id = event_id
        self._event_location = event_location
        self._event_date = event_date
        self._event_status = event_status

    def get_event_id(self):
        return self._event_id

    def get_event_location(self):
        return self._event_location

    def get_event_date(self):
        return self._event_date

    def get_event_status(self):
        return self._event_status

    def set_event_id(self, event_id):
        self._event_id = event_id

    def set_event_location(self, event_location):
        self._event_location = event_location

    def set_event_date(self, event_date):
        self._event_date = event_date

    def set_event_status(self, event_status):
        self._event_status = event_status