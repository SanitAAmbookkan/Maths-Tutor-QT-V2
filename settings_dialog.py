# settings_dialog.py
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QSlider, QHBoxLayout,
    QDialogButtonBox, QComboBox
)
from PyQt5.QtCore import Qt
from shared_constants import DIFFICULTY_LEVELS, LANGUAGES

class SettingsDialog(QDialog):
    def __init__(self, parent=None, initial_difficulty=1, current_language="English"):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setMinimumWidth(350)

        layout = QVBoxLayout()

        # ----- Difficulty Level -----
        difficulty_layout = QVBoxLayout()
        label_row = QHBoxLayout()

        difficulty_label = QLabel("Difficulty Level:")
        self.difficulty_name = QLabel(DIFFICULTY_LEVELS[initial_difficulty])
        self.difficulty_name.setStyleSheet("font-weight: bold")

        label_row.addWidget(difficulty_label)
        label_row.addStretch()
        label_row.addWidget(self.difficulty_name)

        self.difficulty_slider = QSlider(Qt.Horizontal)
        self.difficulty_slider.setMinimum(0)
        self.difficulty_slider.setMaximum(len(DIFFICULTY_LEVELS) - 1)
        self.difficulty_slider.setValue(initial_difficulty)
        self.difficulty_slider.setTickInterval(1)
        self.difficulty_slider.setTickPosition(QSlider.TicksBelow)
        self.difficulty_slider.valueChanged.connect(self.update_difficulty_label)

        difficulty_layout.addLayout(label_row)
        difficulty_layout.addWidget(self.difficulty_slider)

        # ----- Language Selection -----
        language_layout = QHBoxLayout()
        language_label = QLabel("Language:")
        self.language_combo = QComboBox()
        self.language_combo.addItems(LANGUAGES)
        self.language_combo.setCurrentText(current_language)

        language_layout.addWidget(language_label)
        language_layout.addStretch()
        language_layout.addWidget(self.language_combo)

        # ----- Placeholder for 3rd Option -----
        third_label = QLabel("More settings coming soon...")
        third_label.setStyleSheet("color: gray; font-style: italic")

        # ----- Dialog Buttons -----
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        # ----- Final Layout -----
        layout.addLayout(difficulty_layout)
        layout.addSpacing(10)
        layout.addLayout(language_layout)
        layout.addSpacing(10)
        layout.addWidget(third_label)
        layout.addStretch()
        layout.addWidget(button_box)

        self.setLayout(layout)

    def update_difficulty_label(self, value):
        self.difficulty_name.setText(DIFFICULTY_LEVELS[value])

    def get_difficulty_index(self):
        return self.difficulty_slider.value()

    def get_selected_language(self):
        return self.language_combo.currentText()
