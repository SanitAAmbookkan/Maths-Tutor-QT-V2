from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt

def create_question_widget(question_text, answer):
    from pages.shared_ui import create_label  # avoid circular imports

    widgets = []

    print(f"[QUESTION SHOWN ON UI] {question_text}")  # Terminal logging

    question_label = create_label(question_text, font_size=14)

    input_box = QLineEdit()
    input_box.setPlaceholderText("Your answer...")

    result_label = QLabel("")
    result_label.setAlignment(Qt.AlignCenter)

    def check_answer():
        try:
            user_answer = float(input_box.text().strip())
            if user_answer == answer:
                result_label.setText("✅ Correct!")
            else:
                result_label.setText(f"❌ Wrong. Correct answer is {answer}")
        except Exception as e:
            result_label.setText(f"Error: {str(e)}")

    submit_button = QPushButton("Submit")
    submit_button.clicked.connect(check_answer)

    widgets.extend([question_label, input_box, submit_button, result_label])
    return widgets
