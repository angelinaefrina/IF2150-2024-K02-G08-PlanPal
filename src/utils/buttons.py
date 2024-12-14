import flet as ft

fonts = {
    "Header": "C:/Users/Lenovo/Documents/RPL/tubes/PlanPal/src/assets/fonts/Fredoka/Fredoka-SemiBold.ttf",
    "Default_Bold": "C:/Users/Lenovo/Documents/RPL/tubes/PlanPal/src/assets/fonts/Afacad/Afacad-Bold.ttf",
    "Default_Regular": "C:/Users/Lenovo/Documents/RPL/tubes/PlanPal/src/assets/fonts/Afacad/Afacad-Regular.ttf",
}
class CreateNewEvent(ft.Container):
    def __init__(self, width=1000, height=50, on_click_action=None, font_family=None):
        super().__init__()
        self.width = width
        self.height = height

        # Button for creating new events
        self.content = ft.ElevatedButton(
            text="Create New Event",
            style=ft.ButtonStyle(
                padding=ft.padding.symmetric(horizontal=50, vertical=20),
                bgcolor="#C4E8F8",
                shape=ft.RoundedRectangleBorder(radius=6),
                text_style=ft.TextStyle(
                    color="#4539B4",
                    weight=ft.FontWeight.BOLD,
                    font_family=font_family,
                    size=26,
                )
            ),
            on_click=on_click_action,
        )

class CreateNewBudget(ft.Container):
    def __init__(self, width=1000, height=50, on_click_action=None, font_family=None):
        super().__init__()
        self.width = width
        self.height = height

        # Button for creating new events
        self.content = ft.ElevatedButton(
            text="Tambah Anggaran Baru",
            style=ft.ButtonStyle(
                padding=ft.padding.symmetric(horizontal=50, vertical=20),
                bgcolor="#C4E8F8",
                shape=ft.RoundedRectangleBorder(radius=6),
                text_style=ft.TextStyle(
                    color="#4539B4",
                    weight=ft.FontWeight.BOLD,
                    font_family=font_family,
                    size=26,
                )
            ),
            on_click=on_click_action,
        )

class EditButton(ft.IconButton):
    def __init__(self, icon_color = "#4539B4", icon_size = 24, on_click_action = None):
        super().__init__(
            icon = ft.icons.EDIT,
            on_click = on_click_action,
            icon_size= icon_size,
            icon_color= icon_color,
            bgcolor= "transparent",
            padding= ft.padding.all(10)
        )

class DeleteButton(ft.IconButton):
    def __init__(self, icon_color = "#FF3D3D", icon_size = 24, on_click_action = None):
        super().__init__(
            icon = ft.icons.DELETE,
            on_click = on_click_action,
            icon_size= icon_size,
            icon_color= icon_color,
            bgcolor= "transparent",
            padding= ft.padding.all(10)
        )

class SaveButton(ft.ElevatedButton):
    def __init__(self, on_click_action = None, font_family=None):
        super().__init__(
            text= "Simpan",
            style= ft.ButtonStyle(
                padding= ft.padding.symmetric(horizontal=30, vertical=10),
                bgcolor= "#C4E8F8",
                shape= ft.RoundedRectangleBorder(radius= 20),
                text_style= ft.TextStyle(
                    color= "#4539B4",
                    weight= ft.FontWeight.BOLD,
                    font_family= font_family,
                    size= 14,
                )
            ),
            on_click= on_click_action
        )

class CancelButton(ft.ElevatedButton):
    def __init__(self, on_click_action = None, font_family=None):
        super().__init__(
            text= "Batal",
            style= ft.ButtonStyle(
                padding= ft.padding.symmetric(horizontal=30, vertical=10),
                bgcolor= "#C4E8F8",
                shape= ft.RoundedRectangleBorder(radius= 20),
                text_style= ft.TextStyle(
                    color= "#4539BA",
                    weight= ft.FontWeight.BOLD,
                    font_family= font_family,
                    size= 14,
                )
            ),
            on_click= on_click_action
        )

class ViewDetailsButton(ft.ElevatedButton):
    def __init__(self, on_click_action = None, font_family=None):
        super().__init__(
            text= "View Details",
            icon= ft.icons.ARROW_FORWARD,
            style= ft.ButtonStyle(
                padding= ft.padding.symmetric(horizontal=30, vertical=10),
                bgcolor= "#C4E8F8",
                shape= ft.RoundedRectangleBorder(radius= 20),
                text_style= ft.TextStyle(
                    color= "#4539B4",
                    weight= ft.FontWeight.BOLD,
                    font_family= font_family,
                    size= 20,
                )
            ),
            on_click= on_click_action
        )

class BackButton(ft.ElevatedButton):
    def __init__(self, on_click_action=None, font_family=None):
        super().__init__(
            text="Back",
            style=ft.ButtonStyle(
                padding=ft.padding.symmetric(horizontal=20, vertical=10),
                bgcolor="#C4E8F8",
                shape=ft.RoundedRectangleBorder(radius=20),
                text_style=ft.TextStyle(
                    color="#4539B4",
                    weight=ft.FontWeight.BOLD,
                    font_family=font_family,
                    size=20,
                ),
            ),
            on_click=on_click_action,
        )
