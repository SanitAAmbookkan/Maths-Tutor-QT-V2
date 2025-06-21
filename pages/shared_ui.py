# pages/shared_ui.py

from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor, QIntValidator
from PyQt5.QtWidgets import QLineEdit
from question.loader import QuestionProcessor
from time import time


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
    back_btn = QPushButton("HOME")
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

from PyQt5.QtWidgets import QWidget, QHBoxLayout

def wrap_center(widget):
    container = QWidget()
    layout = QHBoxLayout()
    layout.addStretch()             # Push from the left
    layout.addWidget(widget)        # The centered widget
    layout.addStretch()             # Push from the right
    container.setLayout(layout)
    return container

class QuestionWidget(QWidget):
    def __init__(self, processor):
        super().__init__()
        self.processor = processor
        self.answer = None
        self.start_time = time()

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)

        self.init_ui()

    def init_ui(self):
        self.question_area = QWidget()
        question_layout = QVBoxLayout()
        question_layout.setAlignment(Qt.AlignCenter)
        self.question_area.setLayout(question_layout)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Arial", 16))
        self.label.setWordWrap(True)

        question_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        question_layout.addWidget(self.label)
        question_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # ✅ Styled input box (your own function)
        self.input_box = create_answer_input()
        self.input_box.returnPressed.connect(self.check_answer)

        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setFont(QFont("Arial", 12))

        # 🧱 Assemble the main layout
        self.layout.addWidget(self.question_area)
        self.layout.addSpacing(20)
        self.layout.addWidget(self.input_box, alignment=Qt.AlignCenter)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.result_label)
        self.layout.addStretch()

        self.load_new_question()

    def load_new_question(self):
        question_text, self.answer = self.processor.get_random_question()
        self.start_time = time()
        self.label.setText(question_text)
        self.input_box.setText("")  # ✨ Clear only the input
        self.result_label.setText("")

    def check_answer(self):
        try:
            user_input = self.input_box.text().strip()
            user_answer = float(user_input)
            elapsed = time() - self.start_time

            correct = float(user_answer) == float(self.answer)
            self.processor.submit_answer(user_answer, self.answer, elapsed)

            if correct:
                self.result_label.setText("✅ Correct!")
                self.load_new_question()  # ✨ Just update content
            else:
                self.result_label.setText(f"❌ Wrong. Try again.")

        except Exception as e:
            self.result_label.setText(f"Error: {str(e)}")



def create_dynamic_question_ui(section_name, difficulty_index, back_callback):
    container = QWidget()
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignTop)
    container.setLayout(layout)

    processor = QuestionProcessor(section_name, difficulty_index)
    processor.process_file()

    question_widget = QuestionWidget(processor)

    layout.addWidget(question_widget)

    # Back Button at the bottom
    back_btn = QPushButton("HOME")
    back_btn.setFixedSize(150, 40)
    back_btn.clicked.connect(back_callback)
    layout.addWidget(back_btn, alignment=Qt.AlignCenter)

    return container
