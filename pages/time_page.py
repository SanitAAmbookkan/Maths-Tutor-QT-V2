from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget
from .shared_ui import create_colored_page

def create_time_page(return_home_callback):
    page = create_colored_page("Time Page", "#FFC107")
    button = QPushButton("Back to Home")
    button.clicked.connect(return_home_callback)
    page.layout().addWidget(button)
    return page
