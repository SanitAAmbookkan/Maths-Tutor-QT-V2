from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton,QApplication
from PyQt5.QtCore import Qt
from time import time  # Add at the top of your UI file
from question.loader import play_sound
import random
from PyQt5.QtCore import QTimer
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
            elapsed = time() - question_start_time

            is_correct = float(user_answer) == float(answer)
            processor.submit_answer(user_answer, answer, elapsed)

            layout = question_label.parent().layout()
            def show_final_score():
                result_label.setText(
                    "🎉 Quiz Finished!"
                )
                print("Final Score:", processor.correct_answers, "/", processor.total_attempts)
                input_box.setDisabled(True)
                submit_button.setDisabled(True)
                sound_index = random.randint(1, 3)
                play_sound(f"finished-{sound_index}.mp3")
            # ✅ Define this ONCE, outside the conditional logic
            def load_next_question():
                if processor.total_attempts >= processor.max_questions:
                    show_final_score()
                    return
                next_q_text, next_answer = processor.get_random_question()

                for widget in widgets:
                    layout.removeWidget(widget)
                    widget.deleteLater()
                widgets.clear()

                new_widgets = create_question_widget(next_q_text, next_answer, processor)
                for w in new_widgets:
                    widgets.append(w)
                    layout.addWidget(w)

            if is_correct:
                result_label.setText("✅ Correct!")
                # Play correct sound
                sound_index = random.randint(1, 3)
                if elapsed < 5:
                    result_label.setText("🌟 Excellent!")
                    play_sound(f"excellent-{sound_index}.mp3")
                elif elapsed < 10:
                    result_label.setText("👍 Very Good!")
                    play_sound(f"very-good-{sound_index}.mp3")
                elif elapsed < 15:
                    result_label.setText("🙂 Good!")
                    play_sound(f"good-{sound_index}.mp3")
                elif elapsed < 20:
                    result_label.setText("😌 Not Bad!")
                    play_sound(f"not-bad-{sound_index}.mp3")
                else:
                    result_label.setText("👌 Okay!")
                    play_sound(f"okay-{sound_index}.mp3")

                processor.retry_count = 0
                QTimer.singleShot(3000, lambda: load_next_question())
            else:
                processor.retry_count += 1
                # Play wrong or repeated wrong sound
                sound_index = random.randint(1, 3)
                if processor.retry_count == 1:
                    play_sound(f"wrong-anwser-{sound_index}.mp3")  # keep the filename typo if that’s how yours are named
                else:
                    play_sound(f"wrong-anwser-repeted-{sound_index}.mp3")
                if processor.retry_count < 3:
                    result_label.setText(f"❌ Wrong. Try again ({processor.retry_count}/3)")
                    
                else:
                    result_label.setText("❌ Wrong. Moving to next question.")
                    
                    processor.retry_count = 0
                    QTimer.singleShot(3000, lambda: load_next_question())

        except Exception as e:
            result_label.setText(f"⚠️ Error: {str(e)}")

    submit_button = QPushButton("Submit")
    submit_button.clicked.connect(check_answer)

    widgets.extend([question_label, input_box, submit_button, result_label])
    return widgets

