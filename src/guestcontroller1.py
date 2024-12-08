class GuestController:
    def __init__(self):
        self.guest_list = []

    def add_guest_list(self, guest_name, rsvp_status):
        guest_id = self.generate_guest_id()  # Menghasilkan ID otomatis
        validation_message = self.validate_guest_list(guest_id, guest_name, rsvp_status)
        if validation_message:
            return validation_message  # Mengembalikan pesan error
        new_guest = {
            "GuestID": guest_id,
            "GuestName": guest_name,
            "RSVPStatus": rsvp_status
        }
        self.guest_list.append(new_guest)
        return "Tamu berhasil ditambahkan."  # Pesan yang lebih sederhana

    def generate_guest_id(self):
        # Menghasilkan GuestID otomatis berdasarkan ID terakhir dalam guest_list
        if self.guest_list:
            # Ambil ID tamu terbesar yang ada
            max_id = max(guest["GuestID"] for guest in self.guest_list)
            return max_id + 1
        return 1  # ID pertama jika daftar tamu kosong

    def validate_guest_list(self, guest_name, rsvp_status):
        if not isinstance(guest_name, str) or not guest_name.strip():
            return "GuestName harus berupa string non-kosong."
        if rsvp_status not in ["Hadir", "Tidak Hadir", "Menyusul"]:
            return "RSVPStatus harus salah satu dari: Hadir, Tidak Hadir, Menyusul."
        return None  # Tidak ada error, validasi sukses

    def edit_guest_list(self, guest_id, new_name=None, new_rsvp_status=None):
        for guest in self.guest_list:
            if guest["GuestID"] == guest_id:
                if new_name:
                    guest["GuestName"] = new_name
                if new_rsvp_status:
                    if new_rsvp_status in ["Hadir", "Tidak Hadir", "Menyusul"]:
                        guest["RSVPStatus"] = new_rsvp_status
                    else:
                        return "RSVPStatus tidak valid. Pembaruan dibatalkan."
                return "Data tamu berhasil diperbarui."  # Pesan yang lebih sederhana
        return "Tamu tidak ditemukan dalam daftar."  # Mengganti pesan error

    def delete_guest_list(self, guest_id):
        for guest in self.guest_list:
            if guest["GuestID"] == guest_id:
                self.guest_list.remove(guest)
                return "Tamu berhasil dihapus."  # Pesan yang lebih sederhana
        return "Tamu tidak ditemukan dalam daftar."  # Mengganti pesan error

    def display_guest_list(self):
        if not self.guest_list:
            return "Daftar tamu kosong."  # Menampilkan jika tamu kosong
        return "\n".join([f"Name: {guest['GuestName']}, RSVPStatus: {guest['RSVPStatus']}" for guest in self.guest_list])
