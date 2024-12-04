from guest import GuestList
from guestcontroller import GuestController
from guestlistform import GuestListForm

def main():
    guest_controller = GuestController()
    guest_form = GuestListForm(guest_controller.guest_list)

    