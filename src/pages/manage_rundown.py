import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import flet as ft
from src.database.rundown import Rundown
from src.database.rundownpage import RundownPage
from src.database.rundowncontroller import RundownController
from src.utils.buttons import *
from src.utils.pagesetup import PageSetup

ITEMS_PER_PAGE = 5
class RundownManagerApp:
    def __init__(self, page, event_id):
        self.page = page
        self.page.title = "Rundown Management"
        self.event_id = event_id

        # Setup page
        self.setup_page()

        # Initialize Controller and Page
        self.rundown_controller = RundownController()
        self.rundown_page = RundownPage(self.rundown_controller)

        self.current_page = 0
        self.create_widgets()
        self.update_display()
    
    def setup_page(self):
        width = self.page.window.width
        height = self.page.window.height
        self.page.bgcolor = '#FFF5E9'

        # Set fonts
        self.page.fonts = {
            "Header": "C:/Users/Lenovo/Documents/RPL/tubes/PlanPal/src/assets/fonts/Fredoka/Fredoka-SemiBold.ttf",
            "Default_Bold": "C:/Users/Lenovo/Documents/RPL/tubes/PlanPal/src/assets/fonts/Afacad/Afacad-Bold.ttf",
            "Default_Regular": "C:/Users/Lenovo/Documents/RPL/tubes/PlanPal/src/assets/fonts/Afacad/Afacad-Regular.ttf",
        }
        # Header PlanPal
        self.page.add(
            ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Text("PlanPal", font_family="Header", color="#FFF5E9", size=64, weight=ft.FontWeight.BOLD),
                        width=width,
                        height=100,
                        bgcolor='#4539B4',
                        padding=ft.padding.all(5),
                        alignment=ft.alignment.top_left
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )
    

    def create_widgets(self):
        self.tree = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Event ID", color= '#4539B4')),
                ft.DataColumn(ft.Text("Nama", color= '#4539B4')),
                ft.DataColumn(ft.Text("Start", color= '#4539B4')),
                ft.DataColumn(ft.Text("End", color= '#4539B4')),
                ft.DataColumn(ft.Text("PIC", color= '#4539B4')),
                ft.DataColumn(ft.Text("")),
            ],
            rows=[],
            bgcolor="#FFF5E9",
            heading_row_color= "#FAEBD9"
        )

        self.title = ft.Text(
            value= "Rundown",
            size= 30,
            weight= ft.FontWeight.BOLD,
            color= "#4539B4",
            font_family= "Default_Bold"
        )

        self.add_button = ft.ElevatedButton(
            text= "Add Rundown",
            style= ft.ButtonStyle(
                padding= ft.padding.symmetric(horizontal=20, vertical=10),
                bgcolor= '#C4E8F8',
                text_style= ft.TextStyle(
                    color= '#4539B4',
                    weight= ft.FontWeight.BOLD,
                    font_family= "Default_Bold",
                    size= 20,
                )
            ),
            color= '#4539B4',
            on_click= self.add_rundown
        )
        
        self.back_button = BackButton(
        on_click_action=self.back_to_event_manager, font_family="Default_Bold"
        )

        self.prev_button = ft.ElevatedButton(text="Prev", on_click=self.prev_page, disabled=True)
        self.next_button = ft.ElevatedButton(text="Next", on_click=self.next_page, disabled=True)

        self.page.add(
            ft.Column(
                [
                    ft.Container(
                        content=self.back_button,
                        alignment=ft.alignment.top_left,
                        padding=ft.padding.all(10),
                    ),
                    ft.Container(
                        content= self.title,
                        alignment= ft.alignment.center,
                        padding= ft.padding.only(bottom=10),
                    ),
                    ft.Container(
                        content= self.add_button,
                        alignment= ft.alignment.center,
                        padding= ft.padding.only(bottom=20),
                    ),
                    ft.Container(
                        content= self.tree,
                        alignment= ft.alignment.top_center,
                        expand= True
                    ),
                    ft.Row(
                        [self.prev_button, self.next_button],
                        alignment= ft.MainAxisAlignment.CENTER,
                        spacing= 20,
                    ),
                ],
                alignment= ft.MainAxisAlignment.START,
                expand= True,
            )
        )

    def add_rundown(self, e, event_id):
        self.rundown_page.display_form(self.page, self.on_form_submit, event_id, is_edit=False)
        
    def back_to_event_manager(self, e):
        from pages.manage_event import EventManagerApp
        # Clear current page content
        self.page.controls.clear()
        # Load EventManagerApp
        EventManagerApp(self.page)
        self.page.update()

    def edit_rundown(self, event_id, agenda_name):
        rundowns = self.rundown_controller.get_rundown_list(event_id)

        print(f"Editing rundown {agenda_name} for event {event_id}")
        rundown_data = next(
            (rundown for rundown in rundowns if rundown["AgendaName"] == agenda_name),
        )

        if rundown_data:
            self.rundown_page.display_form(
                page= self.page,
                on_submit= self.on_form_submit,
                event_id= event_id,
                rundown_data= rundown_data,
                is_edit= True,
            )
        else:
            self.show_error_dialog("Rundown not found.")

    def delete_rundown(self, event_id, agenda_name):
        if self.rundown_controller.get_rundown_list(event_id):
            self.rundown_controller.delete_rundown(event_id, agenda_name)
            self.update_display()

    def update_display(self):
        total_pages = (len(self.rundown_controller.get_all_rundown_list()) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

        self.prev_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page >= total_pages - 1

        start_index = self.current_page * ITEMS_PER_PAGE
        end_index = self.current_page + ITEMS_PER_PAGE

        rundowns = self.rundown_controller.get_all_rundown_list()
        self.tree.rows.clear()
        for rundown in rundowns[start_index:end_index]:
            self.tree.rows.append(
                ft.DataRow(
                    cells=
                    [
                        ft.DataCell(ft.Text(rundown["EventID"])),
                        ft.DataCell(ft.Text(rundown["AgendaName"])),
                        ft.DataCell(ft.Text(rundown["AgendaTimeStart"])),
                        ft.DataCell(ft.Text(rundown["AgendaTimeEnd"])),
                        ft.DataCell(ft.Text(rundown["AgendaPIC"])),
                        ft.DataCell(
                            ft.Row(
                                controls=
                                [
                                    EditButton(on_click_action= lambda e, event_id=rundown["EventID"], agenda_name=rundown["AgendaName"]: self.edit_rundown(event_id, agenda_name)),
                                    DeleteButton(on_click_action= lambda e, event_id=rundown["EventID"], agenda_name=rundown["AgendaName"]: self.delete_rundown(event_id, agenda_name)),
                                ]
                            )
                        ),
                    ]
                )
            )
        self.page.update()

    def prev_page(self, e):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_display()

    def next_page(self, e):
        total_pages = (len(self.rundown_controller.get_all_rundown_list()) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.update_display()

    def on_form_submit(self, form_data, is_edit, event_id):
        # Use time values from TimePickers for AgendaTimeStart and AgendaTimeEnd
        if is_edit:
            self.rundown_controller.edit_rundown(
                event_id,
                form_data["AgendaName"],
                form_data["AgendaTimeStart"].strftime("%H:%M"),  # Convert TimePicker to string
                form_data["AgendaTimeEnd"].strftime("%H:%M"),  # Convert TimePicker to string
                form_data["AgendaPIC"]
            )
        else:
            self.rundown_controller.add_rundown(
                event_id,
                form_data["AgendaName"],
                form_data["AgendaTimeStart"].strftime("%H:%M"),  # Convert TimePicker to string
                form_data["AgendaTimeEnd"].strftime("%H:%M"),  # Convert TimePicker to string
                form_data["AgendaPIC"]
            )
        self.update_display()

    def show_error_dialog(self, message):
        error_dialog = ft.AlertDialog(
            title= ft.Text("Error"),
            content= ft.Text(message),
            actions= [ft.TextButton(text="OK", on_click= lambda e: self.close_error_dialog())]
        )
        self.page.dialog = error_dialog
        error_dialog.open = True
        self.page.update()

    def show_success_dialog(self, message):
        success_dialog = ft.AlertDialog(
            title= ft.Text("Success"),
            content= ft.Text(message),
            actions= [ft.TextButton(text="OK", on_click= lambda e: self.close_success_dialog())]
        )
        self.page.dialog = success_dialog
        success_dialog.open = True
        self.page.update()

    def close_error_dialog(self):
        self.page.dialog.open = False
        self.page.update

    def close_success_dialog(self):
        self.page.dialog.open = False
        self.page.update()


def main(page: ft.Page):
    app = RundownManagerApp(page)

ft.app(target=main)