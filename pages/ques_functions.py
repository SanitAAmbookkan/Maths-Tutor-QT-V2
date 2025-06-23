from PyQt5.QtWidgets import QHBoxLayout, QWidget
from PyQt5.QtCore import Qt

from pages.shared_ui import (
    create_colored_widget,
    create_label,
    create_vertical_layout,
    create_back_button,
    create_menu_button,
    create_answer_input,
    wrap_center,
    create_audio_toggle_button
    
)
from question.loader import get_questions


def load_pages(section_name, back_callback, main_window=None):
    page = create_colored_widget("#e0f7fa")

    widgets = []
    # --- 🏠 Back button at top-left ---
    top_bar = QWidget()
    top_layout = QHBoxLayout(top_bar)
    top_layout.setContentsMargins(0, 0, 0, 0)
    top_layout.addWidget(create_back_button(back_callback), alignment=Qt.AlignLeft)
    top_layout.addStretch()
    widgets.append(top_bar)
    
    # 👉 Custom logic for "Operations"
    if section_name.lower() == "operations":
        widgets.append(create_label("Choose an Operation", font_size=20))
        for sub in ["Addition", "Subtraction", "Multiplication", "Division","Remainder","Percentage"]:
            widgets.append(
                create_menu_button(
                    sub,
                    lambda _, s=sub: main_window.load_section(s)
                )
            )
        #widgets.append(create_back_button(back_callback))
        #page.setLayout(create_vertical_layout(widgets))
        return page

    # 👉 Default logic for all other sections
    widgets.append(create_label(f"{section_name} Section", font_size=20))
    questions = get_questions(section_name)
    for q in questions:
        widgets.append(create_label(q, font_size=14, bold=False))
        widgets.append(wrap_center(create_answer_input()))  # 👈 Call your custom input function here

    #widgets.append(create_back_button(back_callback))
    
     # --- 🔊 Mute button at bottom-left ---
    bottom_bar = QWidget()
    bottom_layout = QHBoxLayout(bottom_bar)
    bottom_layout.setContentsMargins(0, 0, 0, 0)
    bottom_layout.addWidget(create_audio_toggle_button(), alignment=Qt.AlignLeft)
    bottom_layout.addStretch()
    widgets.append(bottom_bar)

    page.setLayout(create_vertical_layout(widgets))
    print(f"[QUESTION SHOWN] {questions}")
    return page

