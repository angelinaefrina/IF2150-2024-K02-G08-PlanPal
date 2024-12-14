import sys
import os

# Add the src directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import flet as ft
from guestcontroller import GuestController
from guestlistform import GuestListForm
from utils.buttons import *
from utils.pagesetup import PageSetup

ITEMS_PER_PAGE = 6
    
def main(page: ft.Page):
    app = GuestManagerApp(page)

if __name__ == "__main__":
    ft.app(target=main)
