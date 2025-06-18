from PyQt5.QtWidgets import QPushButton
from settings_dialog import SettingsDialog
from settings_manager import settings

def create_settings_button(parent_window):
    """
    Creates a reusable 'Settings' button you can add to any window.
    """
    btn = QPushButton("Settings")
    btn.clicked.connect(lambda: open_settings_dialog(parent_window))
    return btn

def open_settings_dialog(parent_window):
    """
    Opens the Settings dialog and updates global settings if confirmed.
    """
    dialog = SettingsDialog(
        parent=parent_window,
        initial_difficulty=settings.get_difficulty(),
        current_language=settings.get_language()
    )

    if dialog.exec_():
        # Update the global state
        settings.set_difficulty(dialog.get_difficulty_index())
        settings.set_language(dialog.get_selected_language())

        # Debug/logging
        print("[✅ SETTINGS UPDATED]")
        print("   Difficulty Index:", settings.get_difficulty())
        print("   Language:", settings.get_language())
