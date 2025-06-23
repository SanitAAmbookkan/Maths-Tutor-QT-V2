# pages/shared_ui.py

from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QPalette, QColor, QIntValidator
from PyQt5.QtWidgets import QLineEdit, QWidget, QHBoxLayout


def create_colored_widget(color: str = "#ffffff") -> QWidget:
    widget = QWidget()
    palette = widget.palette()
    palette.setColor(QPalette.Window, QColor(color))
    widget.setAutoFillBackground(True)
    widget.setPalette(palette)
    return widget

def create_label(text: str, font_size=50, bold=True) -> QLabel:
    label = QLabel(text)
    label.setAlignment(Qt.AlignCenter)
    font = QFont("Arial", font_size)
    font.setBold(bold)
    label.setFont(font)
    return label

def create_colored_page(title: str, color: str = "#518c33") -> QWidget:
    page = create_colored_widget(color)
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignCenter)

    title_label = create_label(title, font_size=20)
    answer_input = create_answer_input()

    layout.addWidget(title_label)
    layout.addSpacing(20)
    layout.addWidget(answer_input)

    page.setLayout(layout)
    return page


def create_menu_button(text, callback):
    button = QPushButton(text)
    button.setFixedSize(200, 40)
    button.setProperty("class", "menu-button")
    button.clicked.connect(callback)
    return button

def create_vertical_layout(widgets: list) -> QVBoxLayout:
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignCenter)
    for widget in widgets:
        layout.addWidget(widget)
    return layout

def create_back_button(callback) -> QPushButton:
    back_btn = QPushButton("🏠")
    back_btn.setObjectName("home")
    back_btn.setFixedSize(150, 40)
    back_btn.setProperty("class", "menu-button")
    back_btn.clicked.connect(callback)
    return back_btn


def create_answer_input(width=300, height=40, font_size=14) -> QLineEdit:
    input_box = QLineEdit()
    input_box.setFixedSize(width, height)
    input_box.setAlignment(Qt.AlignCenter)
    input_box.setPlaceholderText("Enter your answer")
    input_box.setFont(QFont("Arial", font_size))
    input_box.setValidator(QIntValidator(0, 1000000))  # only positive integers
    input_box.setStyleSheet("""
        QLineEdit {
            border: 2px solid #ccc;
            border-radius: 10px;
            padding: 6px 10px;
        }
        QLineEdit:focus {
            border: 2px solid #0078d7;
            background-color: #f0f8ff;
        }
    """)
    return input_box

def wrap_center(widget):
    container = QWidget()
    layout = QHBoxLayout()
    layout.addStretch()             # Push from the left
    layout.addWidget(widget)        # The centered widget
    layout.addStretch()             # Push from the right
    container.setLayout(layout)
    return container


#audio_button
audio_muted = False

def toggle_audio(button: QPushButton):
    global audio_muted
    audio_muted = not audio_muted
    update_audio_icon(button)
    print("Muted" if audio_muted else "Unmuted")

def update_audio_icon(button: QPushButton):
    icon = "🔇" if audio_muted else "🔊"
    button.setText(icon)
    button.setToolTip("Unmute" if audio_muted else "Mute")
    button.setProperty("audioMuted", audio_muted)
    button.style().unpolish(button)
    button.style().polish(button)

def create_audio_toggle_button() -> QPushButton:
    button = QPushButton()
    button.setObjectName("audioButton")
    button.setFixedSize(QSize(50, 50))
    update_audio_icon(button)
    button.setFocusPolicy(Qt.StrongFocus)  # Accept keyboard focus
    button.setDefault(True)  # Allow Enter key to work

    # Connect both mouse click and Enter key
    button.clicked.connect(lambda: toggle_audio(button))

    return button

