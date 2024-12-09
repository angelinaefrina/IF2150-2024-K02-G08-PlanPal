class GuestController:
    def __init__(self):
        self.guest_list = []

    def add_guest_list(self, guest_id, guest_name, rsvp_status):
        if self.validate_guest_list(guest_id, guest_name, rsvp_status):
            new_guest = {
                "GuestID": guest_id,
                "GuestName": guest_name,
                "RSVPStatus": rsvp_status
            }
            self.guest_list.append(new_guest)
            print(f"Tamu dengan ID {guest_id} berhasil ditambahkan.")
        else:
            print("Data tamu tidak valid. Penambahan tamu dibatalkan.")

    def validate_guest_list(self, guest_id, guest_name, rsvp_status):
        if not isinstance(guest_id, int) or guest_id <= 0:
            print("GuestID harus berupa angka positif.")
            return False
        if not isinstance(guest_name, str) or not guest_name.strip():
            print("GuestName harus berupa string non-kosong.")
            return False
        if rsvp_status not in ["Accepted", "Declined", "Pending"]:
            print("RSVPStatus harus salah satu dari: Accepted, Declined, Pending.")
            return False
        if any(guest["GuestID"] == guest_id for guest in self.guest_list):
            print(f"GuestID {guest_id} sudah ada dalam daftar.")
            return False

        return True
class GuestController:
    def __init__(self):
        self.guest_list = []
        self._next_guest_id = 1  # Start ID from 1

    def add_guest_list(self, guest_name, rsvp_status):
        if self.validate_guest_list(guest_name, rsvp_status):
            new_guest = {
                "GuestID": self._next_guest_id,
                "GuestName": guest_name,
                "RSVPStatus": rsvp_status,
            }
            self.guest_list.append(new_guest)
            self._next_guest_id += 1  # Increment ID for the next guest
            print(f"Tamu '{guest_name}' berhasil ditambahkan dengan ID {new_guest['GuestID']}.")
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

    def edit_guest_list(self, guest_id, new_name=None, new_rsvp_status=None):
        for guest in self.guest_list:
            if guest["GuestID"] == guest_id:
                if new_name:
                    guest["GuestName"] = new_name
                if new_rsvp_status:
                    if new_rsvp_status in ["Hadir", "Tidak Hadir", "Menyusul"]:
                        guest["RSVPStatus"] = new_rsvp_status
                    else:
                        print("RSVPStatus tidak valid. Pembaruan dibatalkan.")
                        return
                print(f"Data tamu dengan ID {guest_id} berhasil diperbarui.")
                return
        print(f"GuestID {guest_id} tidak ditemukan dalam daftar.")

    def delete_guest_list(self, guest_id):
        for guest in self.guest_list:
            if guest["GuestID"] == guest_id:
                self.guest_list.remove(guest)
                print(f"Tamu dengan ID {guest_id} berhasil dihapus.")
                return
        print(f"GuestID {guest_id} tidak ditemukan dalam daftar.")

    def display_guest_list(self):
        if not self.guest_list:
            print("Daftar tamu kosong.")
            return
        print("Daftar Tamu:")
        for guest in self.guest_list:
            print(f"- GuestID: {guest['GuestID']}, Name: {guest['GuestName']}, RSVPStatus: {guest['RSVPStatus']}")