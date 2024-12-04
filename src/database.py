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

    def close_connection(self):
        self.connection.close()

class EventDatabase(Database):
    def create_event_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS Event (
            EventID INTEGER PRIMARY KEY AUTOINCREMENT,
            EventLocation TEXT NOT NULL,
            EventDate DATE NOT NULL,
            EventStatus TEXT NOT NULL CHECK(EventStatus IN ('Selesai', 'Belum dimulai', 'Berlangsung', 'Batal'))
        );
        """
        self.execute_query(query)

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

class RundownDatabase(Database):
    def create_rundown_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS Rundown (
            EventID INTEGER NOT NULL,
            AgendaName TEXT NOT NULL,
            AgendaTimeStart TIME NOT NULL,
            AgendaTimeEnd TIME NOT NULL,
            AgendaDuration TIME NOT NULL,
            AgendaPIC TEXT NOT NULL,
            FOREIGN KEY(EventID) REFERENCES Event(EventID)
        );
        """
        self.execute_query(query)

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