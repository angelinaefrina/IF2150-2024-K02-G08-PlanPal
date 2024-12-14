import flet as ft

class PageSetup:
# ===== PAGE SETUP =====
    def __init__(self, page: ft.Page):
        self.page = page
        self.setup_page()
    
    def setup_page(self):
        width = self.page.window.width
        height = self.page.window.height
        self.page.bgcolor = '#FFF5E9'

        self.page.fonts = {
            "Header": "C:/Users/Lenovo/Documents/RPL/tubes/PlanPal/src/assets/fonts/Fredoka/Fredoka-SemiBold.ttf",
            "Default_Bold": "C:/Users/Lenovo/Documents/RPL/tubes/PlanPal/src/assets/fonts/Afacad/Afacad-Bold.ttf",
            "Default_Regular": "C:/Users/Lenovo/Documents/RPL/tubes/PlanPal/src/assets/fonts/Afacad/Afacad-Regular.ttf",
        }

        self.page.add(
                    ft.Container(
                        content = ft.Text("PlanPal", font_family= "Header", color="#FFF5E9", size=64, weight=ft.FontWeight.BOLD),
                        width= width,
                        height= 100,
                        bgcolor= '#4539B4',
                        padding= ft.padding.all(5),
                        alignment= ft.alignment.top_left
                    )
        )


# def main(page: ft.Page):
#     PageSetup(page)

# ft.app(target=main)