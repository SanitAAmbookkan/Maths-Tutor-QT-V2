# pages/story_page.py

from .shared_ui import QWidget, QVBoxLayout, create_label, create_colored_widget,QPushButton


def create_story_page(return_home_callback):
    page = create_colored_widget("#fdf1dc")
    layout = QVBoxLayout()
    layout.addWidget(create_label("Story Page", font_size=18))

    back_button = QPushButton("Back to Home")
    back_button.clicked.connect(return_home_callback)
    layout.addWidget(back_button)

    page.setLayout(layout)
    return page
