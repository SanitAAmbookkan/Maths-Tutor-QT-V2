from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QSlider,
    QHBoxLayout, QDialogButtonBox, QComboBox
)
from PyQt5.QtCore import Qt
from shared_constants import DIFFICULTY_LEVELS, LANGUAGES
from settings_manager import settings  # global singleton


class SettingsDialog(QDialog):
    def __init__(self, parent=None, initial_difficulty=1, current_language="English"):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setFixedSize(400, 220)

        self.difficulty_slider = QSlider(Qt.Horizontal)
        self.difficulty_slider.setMinimum(0)
        self.difficulty_slider.setMaximum(len(DIFFICULTY_LEVELS) - 1)
        self.difficulty_slider.setSingleStep(1)
        self.difficulty_slider.setPageStep(1)
        self.difficulty_slider.setValue(settings.get_difficulty())
        self.difficulty_slider.setTickInterval(1)
        self.difficulty_slider.setTickPosition(QSlider.TicksBelow)
        self.difficulty_slider.setFocusPolicy(Qt.StrongFocus)
        self.difficulty_slider.setFocus()

        self.difficulty_label = QLabel(DIFFICULTY_LEVELS[settings.get_difficulty()])
        self.difficulty_label.setAlignment(Qt.AlignCenter)
        self.difficulty_label.setStyleSheet("font-weight: bold; font-size: 16px;")

        self.difficulty_slider.valueChanged.connect(self.update_difficulty_label)

        # Language ComboBox
        self.language_combo = QComboBox()
        self.language_combo.addItems(LANGUAGES)
        self.language_combo.setCurrentText(settings.get_language())

        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept_settings)
        button_box.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Select Difficulty:"))
        layout.addWidget(self.difficulty_slider)
        layout.addWidget(self.difficulty_label)
        layout.addSpacing(15)
        layout.addWidget(QLabel("Select Language:"))
        layout.addWidget(self.language_combo)
        layout.addSpacing(10)
        layout.addWidget(button_box)
        self.setLayout(layout)

    def update_difficulty_label(self, index):
        self.difficulty_label.setText(DIFFICULTY_LEVELS[index])

    def accept_settings(self):
        index = self.difficulty_slider.value()
        settings.set_difficulty(index)
        settings.set_language(self.language_combo.currentText())
        
        print(f"Difficulty index set to: {index}")
    
        self.accept()

    def get_difficulty_index(self):
        return self.difficulty_slider.value()

    def get_selected_language(self):
        return self.language_combo.currentText()     