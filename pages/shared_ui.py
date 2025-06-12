# pages/shared_ui.py

from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor

def create_colored_widget(color: str = "#ffffff") -> QWidget:
    widget = QWidget()
    palette = widget.palette()
    palette.setColor(QPalette.Window, QColor(color))
    widget.setAutoFillBackground(True)
    widget.setPalette(palette)
    return widget

def create_label(text: str, font_size=16, bold=True) -> QLabel:
    label = QLabel(text)
    label.setAlignment(Qt.AlignCenter)
    font = QFont("Arial", font_size)
    font.setBold(bold)
    label.setFont(font)
    return label

def create_colored_page(title: str, color: str = "#d0f0c0") -> QWidget:
    page = create_colored_widget(color)
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignCenter)
    layout.addWidget(create_label(title, font_size=20))
    page.setLayout(layout)
    return page

def create_menu_button(text: str, callback) -> QPushButton:
    button = QPushButton(text)
    button.setFixedSize(150, 40)
    button.setProperty("class", "menu-button")
    button.clicked.connect(callback)
    return button
