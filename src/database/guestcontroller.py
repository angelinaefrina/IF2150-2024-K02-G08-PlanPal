class GuestController:
    def __init__(self):
        self.guest_list = []
        self._next_guest_id = 1  # Start ID from 1

    def add_guest_list(self, event_id, guest_name, rsvp_status):
        if self.validate_guest_list(guest_name, rsvp_status):
            new_guest = {
                "EventID": event_id,
                "GuestID": self._next_guest_id,
                "GuestName": guest_name,
                "RSVPStatus": rsvp_status,
            }
            self.guest_list.append(new_guest)
            self._next_guest_id += 1  # Increment ID for the next guest
            print(f"Tamu '{guest_name}' berhasil ditambahkan ke Event {event_id} dengan ID {new_guest['GuestID']}.")
        else:
            print("Data tamu tidak valid. Penambahan tamu dibatalkan.")

    def validate_guest_list(self, guest_name, rsvp_status):
        if not isinstance(guest_name, str) or not guest_name.strip():
            print("GuestName harus berupa string non-kosong.")
            return False
        if rsvp_status not in ["Hadir", "Tidak Hadir", "Menyusul"]:
            print("RSVPStatus harus salah satu dari: Hadir, tidak Hadir, Menyusul.")
            return False
        return True

    # Methods edit_guest_list, delete_guest_list, and display_guest_list remain unchanged

    def edit_guest_list(self, event_id, guest_id, new_name=None, new_rsvp_status=None):
        for guest in self.guest_list:
            if guest["EventID"] == event_id and guest["GuestID"] == guest_id:
                if new_name:
                    guest["GuestName"] = new_name
                if new_rsvp_status:
                    if new_rsvp_status in ["Hadir", "Tidak Hadir", "Menyusul"]:
                        guest["RSVPStatus"] = new_rsvp_status
                    else:
                        print("RSVPStatus tidak valid. Pembaruan dibatalkan.")
                        return
                print(f"Data tamu dengan ID {guest_id} di Event {event_id} berhasil diperbarui.")
                return
        print(f"GuestID {guest_id} tidak ditemukan dalam Event {event_id}.")

    def delete_guest_list(self, event_id, guest_id):
        for guest in self.guest_list:
            if guest["EventID"] == event_id and guest["GuestID"] == guest_id:
                self.guest_list.remove(guest)
                print(f"Tamu dengan ID {guest_id} di Event {event_id} berhasil dihapus.")
                return
        print(f"GuestID {guest_id} tidak ditemukan dalam Event {event_id}.")

    def display_guest_list(self, event_id):
        event_guests = [guest for guest in self.guest_list if guest["EventID"] == event_id]
        print(f"event_guests: {event_guests}")
        if not event_guests:
            print(f"Daftar tamu untuk Event {event_id} masih kosong.")
            return
        print("Daftar Tamu:")
        for guest in event_guests:
            print(f"{event_id} - GuestID: {guest['GuestID']}, Name: {guest['GuestName']}, RSVPStatus: {guest['RSVPStatus']}")

    def get_all_guest_list(self):
        return self.guest_list
    
    def get_guest_list(self, event_id):
        guests = [guest for guest in self.guest_list if guest["EventID"] == event_id]
        if guests:
            return guests
        else:
            print(f"No guests found for EventID {event_id}.")
            return None