class GuestList:
    def __init__(self, event_id=None, guest_id=None, guest_name=None, rsvp_status=None):
        self._event_id = event_id
        self._guest_id = guest_id
        self._guest_name = guest_name
        self._rsvp_status = rsvp_status

    def get_guest_id(self):
        return self._guest_id

    def get_guest_name(self):
        return self._guest_name

    def get_guest_rsvp(self):
        return self._rsvp_status

    def set_guest_id(self, guest_id):
        if isinstance(guest_id, int):
            self._guest_id = guest_id
        else:
            raise ValueError("GuestID harus berupa integer.")

    def set_guest_name(self, guest_name):
        if isinstance(guest_name, str):
            self._guest_name = guest_name
        else:
            raise ValueError("GuestName harus berupa string.")

    def set_rsvp_status(self, rsvp_status):
        if isinstance(rsvp_status, str):
            self._rsvp_status = rsvp_status
        else:
            raise ValueError("RSVPStatus harus berupa string.")