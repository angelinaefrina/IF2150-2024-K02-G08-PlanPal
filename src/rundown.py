from datetime import time

class Rundown:
    def __init__(self, event_id, agenda_name, agenda_time_start, agenda_time_end, agenda_duration, agenda_pic):
        self.event_id = event_id
        self.agenda_name = agenda_name
        self.agenda_time_start = agenda_time_start
        self.agenda_time_end = agenda_time_end
        self.agenda_duration = agenda_duration
        self.agenda_pic = agenda_pic

    def get_rundown(self):
        return {
            "EventID": self.event_id,
            "AgendaName": self.agenda_name,
            "AgendaTimeStart": self.agenda_time_start,
            "AgendaTimeEnd": self.agenda_time_end,
            "AgendaDuration": self.agenda_duration,
            "AgendaPIC": self.agenda_pic
        }

    def get_rundown_by_name(self, agenda_name):
        if self.agenda_name.lower() == agenda_name.lower():
            return self.get_rundown()
        return None

    def get_rundown_by_time_start(self, agenda_time_start):
        if self.agenda_time_start == agenda_time_start:
            return self.get_rundown()
        return None

    def get_rundown_by_pic(self, agenda_pic):
        if self.agenda_pic.lower() == agenda_pic.lower():
            return self.get_rundown()
        return None