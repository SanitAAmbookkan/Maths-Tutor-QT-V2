import sys, os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QDialog, QVBoxLayout,
    QPushButton, QComboBox, QHBoxLayout, QCheckBox, QFrame,
    QWidget, QGridLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy #imported to resize button
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

        languages = ["English", "हिंदी", "മലയാളം", "தமிழ்", "عربي", "संस्कृत"]
        self.language_combo = QComboBox()
        self.language_combo.addItems(languages)
        self.language_combo.setProperty("class", "combo-box")


        self.remember_check = QCheckBox("Remember my selection")
        self.remember_check.setChecked(False)

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
        button_grid.setSpacing(10)
        button_grid.setContentsMargins(10, 10, 10, 10)

        sections = ["Story", "Time", "Currency", "Distance", "Bellring", "Operations"]

        for i, name in enumerate(sections):
            button = QPushButton(name)

            # Set a good preferred base size
            button.setMinimumSize(160, 50)
            button.setMaximumSize(220, 60)  # Optional: Prevent growing too big

             # Use Preferred policy to allow controlled resizing
            button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

            button.setProperty("class", "menu-button")
            button.clicked.connect(lambda checked, n=name: self.load_section(n))

            row, col = divmod(i, 3)
            button_grid.addWidget(button, row, col)

        return button_grid

    def load_section(self, name):
        print(f"[INFO] Loading section: {name}")
        for i in reversed(range(self.main_layout.count())):
            widget = self.main_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        page = load_pages(name, self.back_to_main_menu)  # ← Unified page with questions
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
