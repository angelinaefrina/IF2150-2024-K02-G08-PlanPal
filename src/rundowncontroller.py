class RundownController:
    def __init__(self):
        self.rundown_list = []

    def add_rundown(self, rundown):
        self.rundown_list.append(rundown)
        print(f"Rundown '{rundown.agenda_name}' berhasil ditambahkan.")

    def delete_rundown(self, event_id, agenda_name):
        for rundown in self.rundown_list:
            if rundown.event_id == event_id and rundown.agenda_name.lower() == agenda_name.lower():
                self.rundown_list.remove(rundown)
                print(f"Rundown '{agenda_name}' pada EventID {event_id} berhasil dihapus.")
                return
        print(f"Rundown dengan EventID {event_id} dan Nama Agenda '{agenda_name}' tidak ditemukan.")

    def validate_rundown(self, rundown):
        if not rundown.agenda_name or not rundown.agenda_time_start or not rundown.agenda_time_end or not rundown.agenda_pic:
            print("Data rundown tidak lengkap!")
            return False
        if rundown.agenda_time_start >= rundown.agenda_time_end:
            print("Waktu mulai harus lebih kecil dari waktu selesai.")
            return False
        print("Rundown valid.")
        return True

    def edit_rundown(self, event_id, agenda_name, new_rundown):
        for index, rundown in enumerate(self.rundown_list):
            if rundown.event_id == event_id and rundown.agenda_name.lower() == agenda_name.lower():
                self.rundown_list[index] = new_rundown
                print(f"Rundown '{agenda_name}' pada EventID {event_id} berhasil diperbarui.")
                return
        print(f"Rundown dengan EventID {event_id} dan Nama Agenda '{agenda_name}' tidak ditemukan.")
