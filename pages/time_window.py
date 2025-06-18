from PyQt5.QtWidgets import QPushButton
from settings_dialog import SettingsDialog
from settings_manager import settings

def create_settings_button(parent_window):
    btn = QPushButton("Settings")
    btn.clicked.connect(lambda: open_settings_dialog(parent_window))
    return btn

def open_settings_dialog(parent_window):
    dialog = SettingsDialog(parent=parent_window)
    if dialog.exec_():
        print("Updated Difficulty:", settings.get_difficulty())
        print("Updated Language:", settings.get_language())
        # Optionally: refresh UI or re-load questions
