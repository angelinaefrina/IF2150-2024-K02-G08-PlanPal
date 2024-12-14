class RundownController:
    def __init__(self):
        self.rundown_list = []

    def add_rundown(self, event_id, agenda_name, agenda_time_start, agenda_time_end, agenda_pic):
        # if self.validate_rundown(agenda_time_start, agenda_time_end):
            new_rundown = {
                "EventID": event_id,
                "AgendaName": agenda_name,
                "AgendaTimeStart": agenda_time_start,
                "AgendaTimeEnd": agenda_time_end,
                # "AgendaDuration": int(agenda_time_end) - int(agenda_time_start),
                "AgendaPIC": agenda_pic
            } 
            self.rundown_list.append(new_rundown)
            print(f"Rundown {agenda_name} untuk event {event_id} berhasil ditambahkan.")
        # else:
        #     print("Data rundown tidak valid. Penambahan dibatalkan.")

    def delete_rundown(self, event_id, agenda_name):
        for rundown in self.rundown_list:
            if rundown["EventID"] == event_id and rundown["AgendaName"] == agenda_name:
                self.rundown_list.remove(rundown)
                print(f"Rundown '{agenda_name}' pada EventID {event_id} berhasil dihapus.")
                return
        print(f"Rundown {agenda_name} untuk event {event_id} berhasil ditambahkan.")
       
    def edit_rundown(self, original_event_id, agenda_name, agenda_time_start, agenda_time_end, agenda_pic):
        for rundown in self.rundown_list:
            if rundown["EventID"] == original_event_id:
                rundown["AgendaName"] = agenda_name
                rundown["AgendaTimeStart"] = agenda_time_start
                rundown["AgendaTimeEnd"] = agenda_time_end
                rundown["AgendaPIC"] = agenda_pic
                # rundown["AgendaDuration"] = agenda_time_end - agenda_time_start
                print(f"Updated budget: {rundown}")
                break

    def display_rundown(self, event_id):
        print(f"=== Rundown untuk EventID {event_id} ===")
        event_rundowns = [rundown for rundown in self.rundown_list if rundown["EventID"] == event_id]
        print(f"event_rundowns: {event_rundowns}")
        if not event_rundowns:
            print("No rundowns available to display.")
            return
        print("Rundown:")
        self.arrange_rundown()
        for rundown in event_rundowns:
            print(
                f"- Agenda: {rundown['AgendaName']}, "
                f"Start: {rundown['AgendaTimeStart']}, "
                f"End: {rundown['AgendaTimeEnd']}, "
                f"Duration: {rundown['AgendaDuration']} minutes, "
                f"PIC: {rundown['AgendaPIC']}"
            )
        print("=============================")
    
    def arrange_rundown(self):
        self.rundown_list.sort(key=lambda x: x["AgendaTimeStart"])
            
    # def validate_rundown(self, agenda_time_start, agenda_time_end):
    #     if agenda_time_start >= agenda_time_end:
    #         print("Waktu mulai harus lebih kecil dari waktu selesai.")
    #         return False
    #     return True
    
    def get_all_rundown_list(self):
        return self.rundown_list
    
    def get_rundown_list(self, event_id):
        rundowns = [rundown for rundown in self.rundown_list if rundown["EventID"] == event_id]
        if rundowns:
            return rundowns
        else:
            print(f"Tidak ada rundown untuk event {event_id}.")
            return []
