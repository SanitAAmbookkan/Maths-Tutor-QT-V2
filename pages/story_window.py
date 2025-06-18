from PyQt5.QtWidgets import QPushButton
from settings_dialog import SettingsDialog
from settings_manager import settings

def open_settings_dialog(parent_window):
    dialog = SettingsDialog(
        parent=parent_window,
        initial_difficulty=settings.get_difficulty(),
        current_language=settings.get_language()
    )
    if dialog.exec_():
        settings.set_difficulty(dialog.get_difficulty_index())
        settings.set_language(dialog.get_selected_language())
        print("Updated Difficulty:", settings.get_difficulty())
        print("Updated Language:", settings.get_language())

def create_settings_button(parent_window):
    btn = QPushButton("Settings")
    btn.clicked.connect(lambda: open_settings_dialog(parent_window))
    return btn
