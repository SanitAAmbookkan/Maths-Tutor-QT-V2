from .shared_ui import create_colored_page, QPushButton

def create_currency_page(return_callback):
    page = create_colored_page("Currency Page", color="#4CAF50")
    button = QPushButton("Back to Home")
    button.clicked.connect(return_callback)
    page.layout().addWidget(button)
    return page
