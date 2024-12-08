class GuestListForm:
    def __init__(self, guest_list=None):
        self.guest_list = guest_list if guest_list else []

    def display_guest_list(self):
        if not self.guest_list:
            self.display_error_message("Daftar tamu kosong.")
            return
        print("Daftar Tamu:")
        for guest in self.guest_list:
            print(f"- GuestID: {guest['GuestID']}, Name: {guest['GuestName']}, RSVPStatus: {guest['RSVPStatus']}")

    def display_edit_guest_list(self):
        if not self.guest_list:
            self.display_error_message("Tidak ada tamu yang dapat diubah.")
            return
        try:
            guest_id = int(input("Masukkan GuestID tamu yang ingin diubah: "))
            guest = next((g for g in self.guest_list if g["GuestID"] == guest_id), None)
            if not guest:
                self.display_error(f"Tamu dengan GuestID {guest_id} tidak ditemukan.")
                return
            print(f"Detail tamu saat ini: Name: {guest['GuestName']}, RSVPStatus: {guest['RSVPStatus']}")
            new_name = input("Masukkan nama baru (tekan Enter untuk tidak mengubah): ").strip()
            new_rsvp_status = input("Masukkan RSVPStatus baru (Hadir/Tidak Hadir/Menyusul, tekan Enter untuk tidak mengubah): ").strip()
            if new_name:
                guest["GuestName"] = new_name
            if new_rsvp_status:
                if new_rsvp_status in ["Hadir", "Tidak Hadir", "Menyusul"]:
                    guest["RSVPStatus"] = new_rsvp_status
                else:
                    self.display_error("RSVPStatus tidak valid. Perubahan dibatalkan.")
                    return

            print(f"Tamu dengan GuestID {guest_id} berhasil diperbarui.")
        except ValueError:
            self.display_error("Input harus berupa angka.")

    def display_error_message(self, message):
        print(f"Error: {message}")

    def display_error(self, message):
        print(f"Error: {message}")