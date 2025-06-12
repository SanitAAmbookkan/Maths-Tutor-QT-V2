from .shared_ui import QWidget, QVBoxLayout, QPushButton, create_label, create_colored_widget

def create_operations_page(show_subpage_callback):
    page = create_colored_widget("#f0e8f7")
    layout = QVBoxLayout()
    layout.addWidget(create_label("Operations Page", font_size=18))

    for name in ["Addition", "Subtraction", "Multiplication", "Division"]:
        button = QPushButton(name)
        button.clicked.connect(lambda checked, n=name: show_subpage_callback(n))
        layout.addWidget(button)

    page.setLayout(layout)
    return page