from event import Event
from eventdisplay import EventDisplay
from formevent import FormEvent
from controllerevent import ControllerEvent

# Create instances of the classes
controller = ControllerEvent()
event_display = EventDisplay(controller.get_event_list())

# Add some events
controller.add_event("1", "Location A", "2023-10-01", "Belum dimulai")
controller.add_event("2", "Location B", "2023-10-02", "Sedang berlangsung")
controller.add_event("3", "Location C", "2023-10-03", "Sudah selesai")
event_display.event_list = controller.get_event_list()
# Update the event list in EventDisplay
# event_display.event_list = controller.get_event_list()

# Display the event list
# event_display.display_event_list()

# Display sort options
# event_display.display_sort_options()

while True:
    user_input = input(">>> ")
    if user_input.upper() == "LIST":
        event_display.display_event_list()
    elif user_input.upper() == "ADD":
        form_event = FormEvent()
        form_data = form_event.display_form()
        form_event.submit_form(form_data)
        event_data = form_data
        controller.add_event(event_data["EventID"], event_data["EventLocation"], event_data["EventDate"], event_data["EventStatus"])
        event_display.event_list = controller.get_event_list()
        event_display.display_event_list()
    elif user_input.upper() == "EDIT":
        event_id = input("Masukkan ID acara yang ingin diedit: ")
        if controller.get_event_details(event_id) is None:
            print(f"Error: Event dengan ID '{event_id}' tidak ditemukan.")
        else:
            form_event = FormEvent()
            form_data = form_event.display_form()
            form_event.submit_form(form_data)
            if form_event.event_details:
                controller.edit_event(event_id, **form_event.event_details)
                event_display.event_list = controller.get_event_list()
                event_display.display_event_list()
    elif user_input.upper() == "EXIT":
        break