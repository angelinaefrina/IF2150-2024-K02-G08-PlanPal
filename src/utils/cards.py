import flet as ft
from .buttons import *

class EventCard(ft.Card):
    def __init__(self, event_title, event_date, on_view_details_click=None, on_edit_click=None, on_delete_click=None, font_family=None):
        super().__init__()
        # fonts = 
        self.content = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(f"{event_date}", size=20, weight=ft.FontWeight.BOLD, font_family=font_family),
                            ft.Container(
                                content= ft.Text(event_title, size=26, font_family="Default_Bold", max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
                                width= 200
                            )
                            
                        ],
                        spacing=20, 
                    ),
                    ft.Row(
                        controls=[
                            # Use your custom button classes here
                            # CreateNewEvent().content,
                            ViewDetailsButton(on_click_action=on_view_details_click, font_family=font_family),
                            EditButton(on_click_action=on_edit_click),
                            DeleteButton(on_click_action=on_delete_click),
                        ],
                        spacing=10,
                    ),
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.START,
            ),
            width=350,
            height=150,
            padding=20,
            border_radius=8,
            bgcolor="#F9F9F9",
            alignment=ft.alignment.center,
        )
        self.elevation = 2

class LandingCard(ft.Card):
    def __init__(self, event_title, event_date, on_view_details_click=None, on_edit_click=None, on_delete_click=None, font_family=None):
        super().__init__()
        # fonts = 
        self.content = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(f"{event_date}", size=20, weight=ft.FontWeight.BOLD, font_family=font_family),
                            ft.Container(
                                content= ft.Text(event_title, size=26, font_family="Default_Bold", max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
                                width= 200
                            )
                        ],
                        spacing=20, 
                    ),
                    ft.Row(
                        controls=[
                            # Use your custom button classes here
                            # CreateNewEvent().content,
                            ViewDetailsButton(on_click_action=on_view_details_click, font_family=font_family),
                        ],
                        spacing=10,
                    ),
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.START,
            ),
            width=350,
            height=150,
            padding=20,
            border_radius=8,
            bgcolor="#F9F9F9",
            alignment=ft.alignment.center,
        )
        self.elevation = 2


# # Example usage of the EventCard class
# def main(page: ft.Page):
#     def on_view_details(e):
#         print("View Details clicked")

#     def on_edit(e):
#         print("Edit button clicked")

#     def on_delete(e):
#         print("Delete button clicked")

#     # Instantiate the EventCard
#     event_card = EventCard(
#         event_title="Tech Conference 2024: The Future of Technology in AI and Robotics",
#         event_date="DES 09",
#         on_view_details_click=lambda e: on_view_details(e),
#         on_edit_click=lambda e: on_edit(e),
#         on_delete_click=lambda e: on_delete(e),
#     )

#     # Add the EventCard to the page
#     page.add(event_card)

# ft.app(target=main)
