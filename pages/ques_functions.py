# pages/ques_functions.py

from pages.shared_ui import (
    create_colored_widget,
    create_label,
    create_menu_button,
    create_back_button,
    create_vertical_layout,
    create_dynamic_question_ui
)

import os, shutil
import pandas as pd

from PyQt5.QtWidgets import QFileDialog, QMessageBox, QInputDialog,QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,QPushButton, QLabel, QSizePolicy
from PyQt5.QtCore import Qt



def load_pages(section_name, back_callback, difficulty_index,
               main_window=None):

    page = create_colored_widget("#e0f7fa")
 
    widgets = []
 
    # 👉 Custom logic for "Operations"
    if section_name.lower() == "operations":
        page = create_colored_widget("#e0f7fa")

        title = create_label("Choose an Operation", font_size=22, bold=True)
        title.setAlignment(Qt.AlignCenter)

        grid = QGridLayout()
        grid.setSpacing(20)

        operations = ["Addition", "Subtraction", "Multiplication", "Division", "Remainder", "Percentage"]

        for i, sub in enumerate(operations):
            btn = create_menu_button(sub, lambda _, s=sub: main_window.load_section(s))
            btn.setFixedSize(180, 60)
            grid.addWidget(btn, i // 2, i % 2)  # 2 columns layout

        wrapper = QWidget()
        wrapper.setLayout(grid)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(wrapper)
        layout.addSpacing(30)
        layout.addWidget(create_back_button(back_callback), alignment=Qt.AlignCenter)

        page.setLayout(layout)
        return page

    # ✅ For all other sections, use dynamic question UI
    return create_dynamic_question_ui(section_name, difficulty_index, back_callback,window=main_window)


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
