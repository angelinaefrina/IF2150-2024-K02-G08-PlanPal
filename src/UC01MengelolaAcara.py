import flet as ft
from event import Event
from eventdisplay import EventDisplay
from formevent import FormEvent
from controllerevent import ControllerEvent

class EventManagerApp:
    def __init__(self, page):
        self.page = page
        self.page.title = "Event Manager"
        
        self.controller = ControllerEvent()
        self.event_display = EventDisplay(self.controller.get_event_list())
        self.form_event = FormEvent()
        
        self.controller.add_event(1, "Event A", "Location A", "2023-10-01", "Belum dimulai")
        self.controller.add_event(2, "Event B", "Location B", "2023-10-02", "Sedang berlangsung")
        self.controller.add_event(3, "Event C", "Location C", "2023-10-03", "Sudah selesai")
        self.event_display.event_list = self.controller.get_event_list()
        
        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        self.tree = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Event ID")),
                ft.DataColumn(ft.Text("Event Name")),
                ft.DataColumn(ft.Text("Location")),
                ft.DataColumn(ft.Text("Date")),
                ft.DataColumn(ft.Text("Status")),
                ft.DataColumn(ft.Text("Actions")),
            ],
            rows=[],
        )

        self.add_button = ft.ElevatedButton(text="Add Event", on_click=self.add_event)
        # self.exit_button = ft.ElevatedButton(text="Exit", on_click=self.page.window_close)

        self.page.add(
            self.tree,
            self.add_button
            # self.exit_button,
        )

    def add_event(self, e):
        self.form_event.display_form(self.page, self.on_form_submit, is_edit=False)

    def edit_event(self, event_id):
        event_data = self.controller.get_event_details(event_id)
        if event_data:
            self.form_event.display_form(self.page, self.on_form_submit, event_data, is_edit=True, original_event_id=event_id)
        else:
            self.show_error_dialog(f"Event with ID '{event_id}' not found.")

    def delete_event(self, event_id):
        if self.controller.get_event_details(event_id):
            self.controller.delete_event(event_id)
            self.update_display()
        else:
            self.show_error_dialog(f"Event with ID '{event_id}' not found.")

    def update_display(self):
        self.tree.rows.clear()
        for event in self.event_display.event_list:
            self.tree.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(event["EventID"])),
                        ft.DataCell(ft.Text(event["EventName"])),
                        ft.DataCell(ft.Text(event["EventLocation"])),
                        ft.DataCell(ft.Text(event["EventDate"])),
                        ft.DataCell(ft.Text(event["EventStatus"])),
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    ft.ElevatedButton(text="Edit", on_click=lambda e, event_id=event["EventID"]: self.edit_event(event_id)),
                                    ft.ElevatedButton(text="Delete", on_click=lambda e, event_id=event["EventID"]: self.delete_event(event_id)),
                                ]
                            )
                        ),
                    ]
                )
            )
        self.page.update()

    def on_form_submit(self, form_data, is_edit, original_event_id=None):
        if form_data:
            if is_edit:
                # Check if the new EventID already exists
                if original_event_id != form_data["EventID"] and self.controller.get_event_details(form_data["EventID"]):
                    self.show_error_dialog(f"Event with ID '{form_data['EventID']}' already exists.")
                else:
                    self.controller.delete_event(original_event_id)
                    self.controller.add_event(
                        form_data["EventID"],
                        form_data["EventName"],
                        form_data["EventLocation"],
                        form_data["EventDate"],
                        form_data["EventStatus"]
                    )
            else:
                if original_event_id != form_data["EventID"] and self.controller.get_event_details(form_data["EventID"]):
                    self.show_error_dialog(f"Event with ID '{form_data['EventID']}' already exists.")
                else:
                    self.controller.add_event(
                        form_data["EventID"],
                        form_data["EventName"],
                        form_data["EventLocation"],
                        form_data["EventDate"],
                        form_data["EventStatus"]
                    )
            self.update_display()

    def show_error_dialog(self, message):
        error_dialog = ft.AlertDialog(
            title=ft.Text("Error"),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=lambda e: self.close_error_dialog())]
        )
        self.page.dialog = error_dialog
        error_dialog.open = True
        self.page.update()

    def close_error_dialog(self):
        self.page.dialog.open = False
        self.page.update()

def main(page: ft.Page):
    app = EventManagerApp(page)

ft.app(target=main)