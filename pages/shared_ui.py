# pages/shared_ui.py

from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QPushButton, QVBoxLayout,QSizePolicy, QDialog, QSlider, QDialogButtonBox, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor

DIFFICULTY_LEVELS = ["Very Easy", "Easy", "Medium", "Hard", "Very Hard"]

# settings_manager.py
class SettingsManager:
    def __init__(self):
        self.difficulty_index = 1  # default Medium
        self.language = "English"

    def set_difficulty(self, index):
        self.difficulty_index = index

    def get_difficulty(self):
        return self.difficulty_index

    def set_language(self, lang):
        self.language = lang

    def get_language(self):
        return self.language


# Singleton instance to be imported anywhere
settings = SettingsManager()


def create_colored_widget(color: str = "#ffffff") -> QWidget:
    widget = QWidget()
    palette = widget.palette()
    palette.setColor(QPalette.Window, QColor(color))
    widget.setAutoFillBackground(True)
    widget.setPalette(palette)
    return widget

def create_label(text: str, font_size=16, bold=True) -> QLabel:
    label = QLabel(text)
    label.setWordWrap(True)  # allow wrapping of long text
    label.setAlignment(Qt.AlignCenter)  # center text
    font = QFont("Arial", font_size)
    font.setBold(bold)
    label.setFont(font)
    label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)  # allow resizing
    return label
   

def create_colored_page(title: str, color: str = "#d0f0c0") -> QWidget:
    page = create_colored_widget(color)
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignCenter)
    layout.addWidget(create_label(title, font_size=20))
    page.setLayout(layout)
    return page

def create_menu_button(text, callback):
    button = QPushButton(text)
    button.setFixedSize(200, 40)
    button.setProperty("class", "menu-button")
    button.clicked.connect(callback)
    return button

def create_vertical_layout(widgets: list) -> QVBoxLayout:
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignTop)  # Align to top so everything is visible
    for widget in widgets:
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(widget)
    return layout
   
def create_footer_buttons(names, callbacks=None, size=(90, 30)) -> QWidget:
    footer = QWidget()
    layout = QHBoxLayout()
    layout.setContentsMargins(10, 10, 10, 10)
    layout.addStretch()

    for name in names:
        btn = QPushButton(name)
        btn.setFixedSize(*size)
        btn.setProperty("class", "footer-button")
        if callbacks and name in callbacks:
            btn.clicked.connect(callbacks[name])
        layout.addWidget(btn)

    footer.setLayout(layout)
    return footer


def create_back_button(callback) -> QPushButton:
    back_btn = QPushButton("Back to Menu")
    back_btn.setFixedSize(150, 40)
    back_btn.setProperty("class", "menu-button")
    back_btn.clicked.connect(callback)
    return back_btn

class SettingsDialog(QDialog):
    def __init__(self, parent=None, initial_difficulty=1, main_window=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setFixedSize(400, 220)

        self.main_window = main_window
        self.updated_language = main_window.language if main_window else "English"

        self.difficulty_slider = QSlider(Qt.Horizontal)
        self.difficulty_slider.setMinimum(0)
        self.difficulty_slider.setMaximum(len(DIFFICULTY_LEVELS) - 1)
        self.difficulty_slider.setSingleStep(1)
        self.difficulty_slider.setPageStep(1)
        self.difficulty_slider.setTickInterval(1)
        self.difficulty_slider.setTickPosition(QSlider.TicksBelow)
        self.difficulty_slider.setTracking(True)
        self.difficulty_slider.setFocusPolicy(Qt.StrongFocus)
        self.difficulty_slider.setFocus()
        self.difficulty_slider.setValue(initial_difficulty)
        self.difficulty_slider.valueChanged.connect(self.update_difficulty_label)

        self.difficulty_label = create_label(DIFFICULTY_LEVELS[initial_difficulty], font_size=12)

        # 🔁 Reset Language Button
        self.language_reset_btn = QPushButton("Reset Language")
        self.language_reset_btn.setFixedHeight(30)
        self.language_reset_btn.clicked.connect(self.handle_reset_language)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept_settings)
        button_box.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(create_label("Select Difficulty:", font_size=12, bold=False))
        layout.addWidget(self.difficulty_slider)
        layout.addWidget(self.difficulty_label)
        layout.addSpacing(15)
        layout.addWidget(self.language_reset_btn)
        layout.addSpacing(10)
        layout.addWidget(button_box)
        self.setLayout(layout)

    def update_difficulty_label(self, index):
        self.difficulty_label.setText(DIFFICULTY_LEVELS[index])

    def handle_reset_language(self):
        from main import RootWindow, MainWindow # Dynamically import to avoid circular imports

        dialog = RootWindow()
        if dialog.exec_() == QDialog.Accepted:
            new_lang = dialog.language_combo.currentText()
            self.updated_language = new_lang
            print(f"[Language Reset] New language: {new_lang}")

    def accept_settings(self):
        selected_index = self.difficulty_slider.value()
        settings.set_difficulty(selected_index)
        settings.set_language(self.updated_language)
        print(f"[Difficulty] Index set to: {selected_index}")
        self.accept()

    def get_difficulty_index(self):
        return self.difficulty_slider.value()

    def get_selected_language(self):
        return self.updated_language
        
