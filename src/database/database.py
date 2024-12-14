import sqlite3

class Database:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def execute_query(self, query, parameters=None):
        if parameters is None:
            parameters = []
        self.cursor.execute(query, parameters)
        self.connection.commit()

    def fetch_query(self, query, parameters=None):
        if parameters is None:
            parameters = []
        self.cursor.execute(query, parameters)
        return self.cursor.fetchall()

    def close_connection(self):
        self.connection.close()

class EventDatabase(Database):
    def create_event_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS Event (
            EventID INTEGER PRIMARY KEY AUTOINCREMENT,
            EventName TEXT NO NULL,
            EventLocation TEXT NOT NULL,
            EventDate DATE NOT NULL,
            EventStatus TEXT NOT NULL CHECK(EventStatus IN ('Sudah selesai', 'Belum dimulai', 'Sedang berlangsung', 'Batal'))
        );
        """
        self.execute_query(query)

    def add_event(self, event_id, event_name, event_location, event_date, event_status):
        query = """
        INSERT INTO Event (EventId, EventName, EventLocation, EventDate, EventStatus)
        VALUES (?, ?, ?, ?, ?)
        """
        parameters = (event_id, event_name, event_location, event_date, event_status)
        self.execute_query(query, parameters)
    
    def get_all_events(self):
        query = """
        SELECT * FROM Event
        """
        return self.fetch_query(query)

# ------------------------------ Tabel GuestList ------------------------------
class GuestListDatabase(Database):
    def create_guest_list_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS GuestList (
            EventID INTEGER NOT NULL,
            GuestID INTEGER PRIMARY KEY AUTOINCREMENT,
            GuestName TEXT NOT NULL,
            RSVPStatus TEXT NOT NULL CHECK(RSVPStatus IN ('Hadir', 'Tidak hadir', 'Menyusul', 'Meninggalkan')),
            FOREIGN KEY(EventID) REFERENCES Event(EventID)
        );
        """
        self.execute_query(query)

    def add_guest(self, event_id, guest_name, rsvp_status):
        query = """
        INSERT INTO GuestList (EventID, GuestName, RSVPStatus)
        VALUES (?, ?, ?)
        """
        parameters = (event_id, guest_name, rsvp_status)
        self.execute_query(query, parameters)

    def get_guests_by_event(self, event_id):
        query = """
        SELECT * FROM GuestList WHERE EventID = ?
        """
        return self.fetch_query(query, (event_id,))

class BudgetDatabase(Database):
    def create_budget_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS Budget (
            EventID INTEGER NOT NULL,
            RequirementName TEXT NOT NULL,
            RequirementBudget INTEGER NOT NULL,
            RequirementQuantity INTEGER NOT NULL,
            FOREIGN KEY(EventID) REFERENCES Event(EventID)
        );
        """
        self.execute_query(query)

    def add_budget(self, event_id, requirement_name, requirement_budget, requirement_quantity):
        query = """
        INSERT INTO Budget (EventID, RequirementName, RequirementBudget, RequirementQuantity)
        VALUES (?, ?, ?, ?)
        """
        parameters = (event_id, requirement_name, requirement_budget, requirement_quantity)
        self.execute_query(query, parameters)

    def get_budget_by_event(self, event_id):
        query = """
        SELECT * FROM Budget WHERE EventID = ?
        """
        return self.fetch_query(query, (event_id,))

class VendorDatabase(Database):
    def create_vendor_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS Vendor (
            EventID INTEGER NOT NULL,
            VendorName TEXT NOT NULL,
            VendorContact TEXT NOT NULL,
            VendorProduct TEXT NOT NULL,
            FOREIGN KEY(EventID) REFERENCES Event(EventID)
        );
        """
        self.execute_query(query)

    def add_vendor(self, event_id, vendor_name, vendor_contact, vendor_product):
        query = """
        INSERT INTO Vendor (EventID, VendorName, VendorContact, VendorProduct)
        VALUES (?, ?, ?, ?)
        """
        parameters = (event_id, vendor_name, vendor_contact, vendor_product)
        self.execute_query(query, parameters)

    def edit_vendor(self, event_id, vendor_name, new_vendor_name, new_vendor_contact, new_vendor_product):
        query = """
        UPDATE Vendor
        SET VendorName = ?, VendorContact = ?, VendorProduct = ?
        WHERE EventID = ? AND VendorName = ?
        """
        parameters = (new_vendor_name, new_vendor_contact, new_vendor_product, event_id, vendor_name)
        self.execute_query(query, parameters)

    def delete_vendor(self, event_id, vendor_name):
        query = """
        DELETE FROM Vendor WHERE EventID = ? AND VendorName = ?
        """
        parameters = (event_id, vendor_name)
        self.execute_query(query, parameters)

    def get_vendors_by_event(self, event_id):
        query = """
        SELECT * FROM Vendor WHERE EventID = ?
        """
        return self.fetch_query(query, (event_id,))

class RundownDatabase(Database):
    def create_rundown_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS Rundown (
            EventID INTEGER NOT NULL,
            AgendaName TEXT NOT NULL,
            AgendaTimeStart TIME NOT NULL,
            AgendaTimeEnd TIME NOT NULL,
            AgendaPIC TEXT NOT NULL,
            FOREIGN KEY(EventID) REFERENCES Event(EventID)
        );
        """
        self.execute_query(query)

    def add_rundown(self, event_id, agenda_name, agenda_time_start, agenda_time_end, agenda_pic):
        query = """
        INSERT INTO Rundown (EventID, AgendaName, AgendaTimeStart, AgendaTimeEnd, AgendaPIC)
        VALUES (?, ?, ?, ?, ?)
        """
        parameters = (event_id, agenda_name, agenda_time_start, agenda_time_end, agenda_pic)
        self.execute_query(query, parameters)

    def get_rundown_by_event(self, event_id):
        query = """
        SELECT * FROM Rundown WHERE EventID = ?
        """
        return self.fetch_query(query, (event_id,))

if __name__ == "__main__":
    database_name = "planpal.db"
    event_db = EventDatabase(database_name)
    event_db.create_event_table()
    guest_list_db = GuestListDatabase(database_name)
    guest_list_db.create_guest_list_table()
    budget_db = BudgetDatabase(database_name)
    budget_db.create_budget_table()
    vendor_db = VendorDatabase(database_name)
    vendor_db.create_vendor_table()
    rundown_db = RundownDatabase(database_name)
    rundown_db.create_rundown_table()
    event_db.close_connection()
    guest_list_db.close_connection()
    budget_db.close_connection()
    vendor_db.close_connection()
    rundown_db.close_connection()