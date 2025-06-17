from pages.shared_ui import (
    create_colored_widget,
    create_label,
    create_vertical_layout,
    create_back_button,
    create_menu_button
)
from question.loader import get_questions
from pages.ques_ui import create_question_widget  # ⬅️ Import here

def load_pages(section_name, back_callback, difficulty_index):
    page = create_colored_widget("#e0f7fa")

    widgets = [create_label(f"{section_name} Section", font_size=20)]
    questions = get_questions(section_name, difficulty_index)

    for q, answer in questions:
        widgets.extend(create_question_widget(q, answer))  # ⬅️ Use extracted function

    widgets.append(create_back_button(back_callback))
    page.setLayout(create_vertical_layout(widgets))
    return page
