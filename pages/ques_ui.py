from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from time import time  # Add at the top of your UI file

def create_question_widget(question_text, answer, processor):
    from pages.shared_ui import create_label

    widgets = []

    question_label = create_label(question_text, font_size=14)
    input_box = QLineEdit()
    input_box.setPlaceholderText("Your answer...")
    result_label = QLabel("")
    result_label.setAlignment(Qt.AlignCenter)

    question_start_time = time()  # 🕒 Start timer here

    def check_answer():
        try:
            user_input = input_box.text().strip()
            
            user_answer = float(user_input)
            elapsed = time() - question_start_time  # ⏱ Time taken

            is_correct = float(user_answer) == float(answer)
            processor.submit_answer(user_answer, answer, elapsed)

            if is_correct:
                result_label.setText("✅ Correct!")
# 🔁 Generate next question from processor
                next_q_text, next_answer = processor.get_random_question()

                # 🔁 Clear and update existing UI widgets
                for widget in widgets:
                    widget.deleteLater()
                widgets.clear()

                # 🧠 Recursively build new question widget
                new_widgets = create_question_widget(next_q_text, next_answer, processor)
                for w in new_widgets:
                    widgets.append(w)
                    question_label.parent().layout().addWidget(w)

            else:
                result_label.setText(f"❌ Wrong. Correct answer is {answer}")

        except Exception as e:
            result_label.setText(f"Error: {str(e)}")


    submit_button = QPushButton("Submit")
    submit_button.clicked.connect(check_answer)

    widgets.extend([question_label, input_box, submit_button, result_label])
    return widgets