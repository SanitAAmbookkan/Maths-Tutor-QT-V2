import sys, os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QDialog, QVBoxLayout,
    QPushButton, QComboBox, QHBoxLayout, QCheckBox, QFrame,
    QWidget, QGridLayout
)
from PyQt5.QtCore import Qt
from pages.ques_functions import load_pages  # ← your new function


class RootWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Maths Tutor - Language Selection")
        self.setFixedSize(400, 250)
        self.init_ui()
        self.load_style("language_dialog.qss")

    def init_ui(self):
        title_label = QLabel("Welcome to Maths Tutor!")
        title_label.setProperty("class", "title")

        language_label = QLabel("Select your preferred language:")
        language_label.setProperty("class", "subtitle")

        self.language_combo = QComboBox()
        self.language_combo.addItems(["English", "Español", "Français", "Deutsch", "中文"])
        self.language_combo.setProperty("class", "combo-box")

        self.remember_check = QCheckBox("Remember my selection")
        self.remember_check.setChecked(True)

        self.cancel_button = QPushButton("Cancel")
        self.ok_button = QPushButton("Continue")

        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addSpacing(15)
        layout.addWidget(language_label)
        layout.addWidget(self.language_combo)
        layout.addWidget(self.remember_check)
        layout.addStretch()
        layout.addWidget(self.create_line())
        btns = QHBoxLayout()
        btns.addStretch()
        btns.addWidget(self.cancel_button)
        btns.addWidget(self.ok_button)
        layout.addLayout(btns)

        self.setLayout(layout)
        self.cancel_button.clicked.connect(self.reject)
        self.ok_button.clicked.connect(self.accept)

    def create_line(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        return line

    def load_style(self, qss_file):
        style_path = os.path.join("styles", qss_file)
        if os.path.exists(style_path):
            with open(style_path, "r") as f:
                self.setStyleSheet(f.read())


class MainWindow(QMainWindow):
    def __init__(self, language="English"):
        super().__init__()
        self.setWindowTitle(f"Maths Tutor - {language}")
        self.resize(900, 600)
        self.language = language
        self.init_ui()
        self.load_style("main_window.qss")
        self.difficulty_index = 1 # Default to level 0 (e.g., "Very Easy")


    def init_ui(self):
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        self.menu_widget = QWidget()
        menu_layout = QVBoxLayout()
        menu_layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Welcome to Maths Tutor!")
        title.setAlignment(Qt.AlignCenter)
        title.setProperty("class", "main-title")

        subtitle = QLabel(f"Ready to learn in {self.language}!")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setProperty("class", "subtitle")

        menu_layout.addWidget(title)
        menu_layout.addWidget(subtitle)
        menu_layout.addSpacing(20)
        menu_layout.addLayout(self.create_buttons())

        self.menu_widget.setLayout(menu_layout)
        self.main_layout.addWidget(self.menu_widget)

    def create_buttons(self):
        button_grid = QGridLayout()
        sections = ["Story", "Time", "Currency", "Distance", "Bellring", "Operations"]

        for i, name in enumerate(sections):
            button = QPushButton(name)
            button.setFixedSize(150, 40)
            button.setProperty("class", "menu-button")
            button.clicked.connect(lambda checked, n=name: self.load_section(n))
            row, col = divmod(i, 3)
            button_grid.addWidget(button, row, col)
        settings_button = QPushButton("Settings")
        settings_button.setFixedSize(150, 40)
        settings_button.setProperty("class", "menu-button")
        settings_button.clicked.connect(self.open_settings)

        row, col = divmod(len(sections), 3)
        button_grid.addWidget(settings_button, row, col)

        return button_grid
   

    def load_section(self, name):
        print(f"[INFO] Loading section: {name}")
        for i in reversed(range(self.main_layout.count())):
            
            widget = self.main_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        page = load_pages(name, self.back_to_main_menu, self.difficulty_index)
         # ← Unified page with questions
        self.main_layout.addWidget(page)

    def back_to_main_menu(self):
        for i in reversed(range(self.main_layout.count())):
            widget = self.main_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.main_layout.addWidget(self.menu_widget)
    
    def load_style(self, qss_file):
        path = os.path.join("styles", qss_file)
        if os.path.exists(path):
            with open(path, "r") as f:
                self.setStyleSheet(f.read())

    def open_settings(self):
        self.clear_main_layout()

        settings_widget = QWidget()
        layout = QVBoxLayout()

        title = QLabel("Settings")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Difficulty dropdown
        difficulty_label = QLabel("Select Difficulty:")
        layout.addWidget(difficulty_label)

        self.difficulty_selector = QComboBox()
        self.difficulty_selector.addItems(["Easy", "Medium", "Hard", "Very Hard", "Extreme"])
        self.difficulty_selector.setCurrentIndex(self.difficulty_index-1)
        self.difficulty_selector.currentIndexChanged.connect(self.change_difficulty)

        layout.addWidget(self.difficulty_selector)

    # Back button
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.back_to_main_menu)
        layout.addWidget(back_button)

        settings_widget.setLayout(layout)
        self.main_layout.addWidget(settings_widget)
    def change_difficulty(self, index):
        print(f"[INFO] Difficulty changed to index: {index+1}")
        self.difficulty_index = index+1
    def clear_main_layout(self):
        for i in reversed(range(self.main_layout.count())):
            widget = self.main_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    style_file = os.path.join("styles", "app.qss")
    if os.path.exists(style_file):
        with open(style_file, "r") as f:
            app.setStyleSheet(f.read())

    dialog = RootWindow()
    if dialog.exec_() == QDialog.Accepted:
        window = MainWindow(language=dialog.language_combo.currentText())
        window.show()
        sys.exit(app.exec_())
