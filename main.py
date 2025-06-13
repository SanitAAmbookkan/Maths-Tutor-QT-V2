import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QDialog, QVBoxLayout,
    QPushButton, QComboBox, QHBoxLayout, QCheckBox, QFrame,
    QWidget, QGridLayout
)
from PyQt5.QtCore import Qt

# Import page creators
from pages.story_page import create_story_page
from pages.time_page import create_time_page
from pages.currency_page import create_currency_page
from pages.distance_page import create_distance_page
from pages.bellring_page import create_bellring_page
from pages.operations_page import create_operations_page

def set_accessibility(widget, name, description=None):
    widget.setAccessibleName(name)
    if description:
        widget.setAccessibleDescription(description)



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

        languages = ["English", "Hindi", "Malayalam", "Tamil", "Arabic", "Sanskrit"]
        self.language_combo = QComboBox()
        self.language_combo.addItems(languages)
        self.language_combo.setProperty("class", "combo-box")

# Accessibility: Add accessible text per item
        for i, lang in enumerate(languages):
            self.language_combo.setItemData(i, lang, Qt.AccessibleTextRole)

# Accessibility: Add combo box name and description
        set_accessibility(self.language_combo, "Language Selection", "Select your preferred language from the list")


        # Accessibility: Make each language readable by screen readers
        for i, lang in enumerate(languages):
            self.language_combo.setItemData(i, lang, Qt.AccessibleTextRole)


        self.remember_check = QCheckBox("Remember my selection")
        self.remember_check.setProperty("class", "checkbox")
        self.remember_check.setChecked(True)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setProperty("class", "danger-button")
        self.ok_button = QPushButton("Continue")
        self.ok_button.setProperty("class", "primary-button")

        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.ok_button)

        main_layout.addWidget(title_label)
        main_layout.addSpacing(15)
        main_layout.addWidget(language_label)
        main_layout.addWidget(self.language_combo)
        main_layout.addWidget(self.remember_check)
        main_layout.addStretch()
        main_layout.addWidget(self.create_horizontal_line())
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        self.cancel_button.clicked.connect(self.reject)
        self.ok_button.clicked.connect(self.accept)

    def create_horizontal_line(self):
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
        menu_layout.addLayout(self.create_menu_buttons())

        self.menu_widget.setLayout(menu_layout)

        self.main_layout.addWidget(self.menu_widget)
        self.setCentralWidget(self.central_widget)

    def create_menu_buttons(self):
        button_grid = QGridLayout()
        button_grid.setSpacing(10)

        self.page_creators = {
            "Story": lambda: create_story_page(self.back_to_main_menu),
            "Time": lambda: create_time_page(self.back_to_main_menu),
            "Currency": lambda: create_currency_page(self.back_to_main_menu),
            "Distance": lambda: create_distance_page(self.back_to_main_menu),
            "Bellring": lambda: create_bellring_page(self.back_to_main_menu),
            "Operations": lambda: create_operations_page(self.show_page)
        }

        for i, (name, creator) in enumerate(self.page_creators.items()):
            button = QPushButton(name)
            button.setProperty("class", "menu-button")
            button.setFixedSize(150, 40)
            button.clicked.connect(lambda checked, n=name: self.show_page(n))
            row = i // 3
            col = i % 3
            button_grid.addWidget(button, row, col)

        return button_grid

    def show_page(self, name):
        if name in self.page_creators:
            for i in reversed(range(self.main_layout.count())):
                widget = self.main_layout.itemAt(i).widget()
                if widget is not None:
                    widget.setParent(None)
            page = self.page_creators[name]()
            self.main_layout.addWidget(page)

    def back_to_main_menu(self):
        for i in reversed(range(self.main_layout.count())):
            widget = self.main_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        self.main_layout.addWidget(self.menu_widget)

    def load_style(self, qss_file):
        path = os.path.join("styles", qss_file)
        if os.path.exists(path):
            with open(path, "r") as f:
                self.setStyleSheet(f.read())


if __name__ == "__main__":
    app = QApplication(sys.argv)

    app_style = os.path.join("styles", "app.qss")
    if os.path.exists(app_style):
        with open(app_style, "r") as f:
            app.setStyleSheet(f.read())

    root_window = RootWindow()
    if root_window.exec_() == QDialog.Accepted:
        main_window = MainWindow(language=root_window.language_combo.currentText())
        main_window.show()
        sys.exit(app.exec_())
