from pages.shared_ui import (
    create_colored_widget,
    create_label,
    create_vertical_layout,
    create_back_button
)
from question.loader import get_questions


def load_pages(section_name, back_callback):
    page = create_colored_widget("#e0f7fa")

    # Collect all widgets for layout
    widgets = [create_label(f"{section_name} Section", font_size=20)]
    questions = get_questions(section_name)
    for q in questions:
        widgets.append(create_label(q, font_size=14, bold=False))
    widgets.append(create_back_button(back_callback))

    page.setLayout(create_vertical_layout(widgets))
    return page
