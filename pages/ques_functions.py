# pages/ques_functions.py

from pages.shared_ui import (
    create_colored_widget,
    create_label,
    create_menu_button,
    create_back_button,
    create_vertical_layout,
    create_dynamic_question_ui
)


def load_pages(section_name, back_callback, difficulty_index, main_window=None):
    # 👉 Handle special case for "Operations" menu
    if section_name.lower() == "operations":
        page = create_colored_widget("#000000")
        layout = create_vertical_layout([])

        layout.addWidget(create_label("Choose an Operation", font_size=20))
        for sub in ["Addition", "Subtraction", "Multiplication", "Division", "Remainder", "Percentage"]:
            layout.addWidget(
                create_menu_button(sub, lambda _, s=sub: main_window.load_section(s))
            )
        layout.addWidget(create_back_button(back_callback))

        page.setLayout(layout)
        return page

    # ✅ For all other sections, use dynamic question UI
    return create_dynamic_question_ui(section_name, difficulty_index, back_callback)
