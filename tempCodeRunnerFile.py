import os, shutil
import pandas as pd
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QInputDialog

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
