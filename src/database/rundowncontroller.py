class RundownController:
    def __init__(self, rundown_db):
        self.rundown_db = rundown_db
        self.rundown_list = []
        self.load_rundowns_from_db()

    def load_rundowns_from_db(self):
        """Load all rundowns from the database into the rundown_list."""
        rundowns = self.rundown_db.fetch_query("SELECT * FROM Rundown")
        self.rundown_list = [
            {
                "EventID": row[0],
                "AgendaName": row[1],
                "AgendaTimeStart": row[2],
                "AgendaTimeEnd": row[3],
                "AgendaPIC": row[4],
            }
            for row in rundowns
        ]
        print("Rundowns loaded from database:", self.rundown_list)

    def add_rundown(self, event_id, agenda_name, agenda_time_start, agenda_time_end, agenda_pic):
        new_rundown = {
            "EventID": event_id,
            "AgendaName": agenda_name,
            "AgendaTimeStart": agenda_time_start,
            "AgendaTimeEnd": agenda_time_end,
            "AgendaPIC": agenda_pic,
        }
        # Add to database
        self.rundown_db.add_rundown(event_id, agenda_name, agenda_time_start, agenda_time_end, agenda_pic)
        # Add to local list
        self.rundown_list.append(new_rundown)
        print(f"Rundown {agenda_name} untuk event {event_id} berhasil ditambahkan.")

    def delete_rundown(self, event_id, agenda_name):
        for rundown in self.rundown_list:
            if rundown["EventID"] == event_id and rundown["AgendaName"] == agenda_name:
                # Remove from local list
                self.rundown_list.remove(rundown)
                # Remove from database
                self.rundown_db.execute_query(
                    "DELETE FROM Rundown WHERE EventID = ? AND AgendaName = ?",
                    (event_id, agenda_name),
                )
                print(f"Rundown '{agenda_name}' pada EventID {event_id} berhasil dihapus.")
                return
        print(f"Rundown {agenda_name} untuk event {event_id} tidak ditemukan.")

    def edit_rundown(self, original_event_id, agenda_name, agenda_time_start, agenda_time_end, agenda_pic):
        for rundown in self.rundown_list:
            if rundown["EventID"] == original_event_id and rundown["AgendaName"] == agenda_name:
                # Update local list
                rundown["AgendaTimeStart"] = agenda_time_start
                rundown["AgendaTimeEnd"] = agenda_time_end
                rundown["AgendaPIC"] = agenda_pic
                # Update database
                self.rundown_db.execute_query(
                    """
                    UPDATE Rundown
                    SET AgendaTimeStart = ?, AgendaTimeEnd = ?, AgendaPIC = ?
                    WHERE EventID = ? AND AgendaName = ?
                    """,
                    (agenda_time_start, agenda_time_end, agenda_pic, original_event_id, agenda_name),
                )
                print(f"Rundown '{agenda_name}' untuk event {original_event_id} berhasil diperbarui.")
                return
        print(f"Rundown {agenda_name} untuk event {original_event_id} tidak ditemukan.")

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
                f"PIC: {rundown['AgendaPIC']}"
            )
        print("=============================")

    def arrange_rundown(self):
        self.rundown_list.sort(key=lambda x: x["AgendaTimeStart"])

    def get_all_rundown_list(self):
        return self.rundown_list

    def get_rundown_list(self, event_id):
        rundowns = [rundown for rundown in self.rundown_list if rundown["EventID"] == event_id]
        if rundowns:
            return rundowns
        else:
            print(f"Tidak ada rundown untuk event {event_id}.")
            return []