class GuestList:
    guest_counter = 1  # Counter untuk memberikan ID tamu otomatis

    def __init__(self, event_id=None, guest_name=None, rsvp_status=None):
        self._event_id = event_id
        self._guest_id = GuestList.guest_counter
        self.set_guest_name(guest_name)
        self.set_rsvp_status(rsvp_status)
        GuestList.guest_counter += 1  # Meningkatkan ID tamu setiap kali tamu baru ditambahkan

    def get_guest_id(self):
        return self._guest_id

    def get_event_id(self):
        return self._event_id

    def get_guest_name(self):
        return self._guest_name

    def get_guest_rsvp(self):
        return self._rsvp_status

    def set_guest_name(self, guest_name):
        if isinstance(guest_name, str) and guest_name.strip():
            self._guest_name = guest_name
        else:
            raise ValueError("GuestName harus berupa string non-kosong.")

    def set_rsvp_status(self, rsvp_status):
        valid_status = ["Hadir", "Tidak Hadir", "Menyusul"]
        if rsvp_status in valid_status:
            self._rsvp_status = rsvp_status
        else:
            raise ValueError(f"RSVPStatus harus salah satu dari: {', '.join(valid_status)}")

    def __str__(self):
        return f"Guest(Name: {self._guest_name}, RSVP: {self._rsvp_status})"

    def __repr__(self):
        return f"GuestList(guest_id={self._guest_id}, event_id={self._event_id}, guest_name={self._guest_name}, rsvp_status={self._rsvp_status})"
