class RundownPage:
    def __init__(self, rundown_controller):
        self.rundown_controller = rundown_controller

    def display_rundown(self, event_id):
        if not self.rundown_controller.rundown_list:
            print("No rundowns available to display.")
            return

        self.arrange_rundown()
        rundown_found = False
        for rundown in self.rundown_controller.rundown_list:
            if rundown.event_id == event_id:
                rundown_found = True
                print(f"Event ID: {rundown.event_id}")
                print(f"Agenda Name: {rundown.agenda_name}")
                print(f"Agenda Time Start: {rundown.agenda_time_start}")
                print(f"Agenda Time End: {rundown.agenda_time_end}")
                print(f"Agenda Duration: {rundown.agenda_duration} minutes")
                print(f"Agenda PIC: {rundown.agenda_pic}")
                print("-" * 40)
        
        if not rundown_found:
            self.display_error_message()

    def display_error_message(self):
        print("Error: Data rundown tidak ditemukan atau tidak valid.")

    def arrange_rundown(self):
        if self.rundown_controller.rundown_list:
            self.rundown_controller.rundown_list.sort(key=lambda rundown: rundown.agenda_time_start)
            print("Rundown has been arranged from the earliest to the latest time.")
