from .shared_ui import QWidget, QVBoxLayout, QPushButton, create_label, create_colored_widget

def create_subtraction_page(return_home_callback):
    page = create_colored_widget("#fddede")
    layout = QVBoxLayout()
    layout.addWidget(create_label("Subtraction Page", font_size=18))

    back_button = QPushButton("Back to Home")
    back_button.clicked.connect(return_home_callback)
    layout.addWidget(back_button)

    page.setLayout(layout)
    return page