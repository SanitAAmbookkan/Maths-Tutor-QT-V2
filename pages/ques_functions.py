from pages.shared_ui import (
    create_colored_widget,
    create_label,
    create_vertical_layout,
    create_back_button,
    create_menu_button
)
from question.loader import get_questions

def load_pages(section_name, back_callback, main_window=None):
    page = create_colored_widget("#e0f7fa")

    widgets = []

    # 👉 Custom logic for "Operations"
    if section_name.lower() == "operations":
        widgets.append(create_label("Choose an Operation", font_size=20))
        for sub in ["Addition", "Subtraction", "Multiplication", "Division"]:
            widgets.append(
                create_menu_button(
                    sub,
                    lambda _, s=sub: main_window.load_section(s)
                )
            )
        widgets.append(create_back_button(back_callback))
        page.setLayout(create_vertical_layout(widgets))
        return page

    # 👉 Default logic for all other sections
    widgets.append(create_label(f"{section_name} Section", font_size=20))
    questions = get_questions(section_name)
    for q in questions:
        widgets.append(create_label(q, font_size=14, bold=False))
    widgets.append(create_back_button(back_callback))

    page.setLayout(create_vertical_layout(widgets))
    print(f"[QUESTION SHOWN] {questions}")
    return page
