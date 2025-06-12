from .shared_ui import QWidget, QPushButton, create_colored_page, QVBoxLayout

def create_bellring_page(return_home_callback):
    page = create_colored_page("Bellring Page", "#FFD54F")
    button = QPushButton("Back to Home")
    button.clicked.connect(return_home_callback)
    page.layout().addWidget(button)
    return page
