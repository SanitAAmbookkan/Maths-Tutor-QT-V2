from pages.shared_ui import (
    create_colored_widget,
    create_label,
    create_vertical_layout,
    create_back_button,
    create_menu_button,
    create_answer_input,
    wrap_center,
    
)
from question.loader import get_questions
import os, shutil
import pandas as pd

from PyQt5.QtWidgets import QFileDialog, QMessageBox, QInputDialog

def load_pages(section_name, back_callback, main_window=None):
    page = create_colored_widget("#e0f7fa")
    widgets = []


    # 👉 Custom logic for "Operations"
    if section_name.lower() == "operations":
        widgets.append(create_label("Choose an Operation", font_size=20))
        for sub in ["Addition", "Subtraction", "Multiplication", "Division", "Remainder", "Percentage"]:
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
        widgets.append(wrap_center(create_answer_input()))  # 👈 Call your custom input function here

    widgets.append(create_back_button(back_callback))

    page.setLayout(create_vertical_layout(widgets))
    print(f"[QUESTION SHOWN] {questions}")
    return page


def upload_excel_with_code(parent_widget, access_code="teacher123", dest_folder="question"):
    code, ok = QInputDialog.getText(parent_widget, "Access Code", "Enter Teacher Code:")
    if not ok or code != access_code:
        QMessageBox.critical(parent_widget, "Access Denied", "Incorrect code.")
        return

    file_path, _ = QFileDialog.getOpenFileName(parent_widget, "Select Excel File", "", "Excel Files (*.xlsx)")
    if not file_path:
        return

    try:
        df = pd.read_excel(file_path)
        required = {"type", "input", "output"}
        if not required.issubset(df.columns):
            QMessageBox.critical(parent_widget, "Invalid File", "Excel must have columns: type, input, output")
            return

        os.makedirs(dest_folder, exist_ok=True)
        dest_path = os.path.join(dest_folder, "question.xlsx")
        shutil.copyfile(file_path, dest_path)
        QMessageBox.information(parent_widget, "Success", "Questions uploaded successfully!")

    except Exception as e:
        QMessageBox.critical(parent_widget, "Error", f"Failed to upload: {e}")
