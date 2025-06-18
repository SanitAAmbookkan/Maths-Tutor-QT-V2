import sys, os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QDialog, QVBoxLayout,
    QPushButton, QComboBox, QHBoxLayout, QCheckBox, QFrame,
    QWidget, QGridLayout
)
from PyQt5.QtWidgets import QStackedWidget, QSizePolicy
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

        languages = ["English", "हिंदी", "മലയാളം", "தமிழ்", "عربي", "संस्कृत"]
        self.language_combo = QComboBox()
        self.language_combo.addItems(languages)
        self.language_combo.setProperty("class", "combo-box")


        self.remember_check = QCheckBox("Remember my selection")
        self.remember_check.setChecked(False)

        self.cancel_button = QPushButton("Cancel")
        self.ok_button = QPushButton("Continue")

        self.ok_button.setDefault(True) #default enter - continue
        self.ok_button.setFocus()

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
        self.setMinimumSize(800, 550)  # Prevents squashing

        self.language = language
        self.init_ui()
        self.load_style("main_window.qss")

    def init_ui(self):
        self.central_widget = QWidget()
        #self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.central_widget.setLayout(self.main_layout)
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
      # menu_layout.addLayout(self.create_buttons())
          # Wrap the grid in a widget with spacing
      #  button_widget = QWidget()
     #   button_layout = QVBoxLayout()
        #button_layout.addLayout(self.create_buttons())
      #  button_layout.addWidget(self.create_buttons())  # ✅ CORRECT

      #  button_layout.addStretch()
     #   button_widget.setLayout(button_layout)
       # menu_layout.addWidget(button_widget)

        menu_layout.addLayout(self.create_buttons())  # ✅ Now adding layout directly


        self.menu_widget.setLayout(menu_layout)
       #self.main_layout.addWidget(self.menu_widget) NEW THINGS:-
        self.stack = QStackedWidget()
        self.stack.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.stack.addWidget(self.menu_widget)
        self.main_layout.addWidget(self.stack)

      #  self.main_layout.addStretch() #new
        footer = self.create_footer_buttons()
        footer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.main_layout.addWidget(footer)
        #self.main_layout.addWidget(self.create_footer_buttons())   new

    def create_buttons(self):
        button_grid = QGridLayout()
        button_grid.setSpacing(10)  # Less vertical & horizontal spacing
        sections = ["Story", "Time", "Currency", "Distance", "Bellring", "Operations"]

        for i, name in enumerate(sections):
            button = QPushButton(name)
            button.setFixedSize(150, 40)
            button.setProperty("class", "menu-button")
            button.clicked.connect(lambda checked, n=name: self.load_section(n))
            row, col = divmod(i, 3)
            button_grid.addWidget(button, row, col)
        return button_grid

            # Create a wrapper widget with fixed height to avoid being pushed off
  #     wrapper = QWidget()
        #wrapper.setLayout(button_grid)
       # wrapper.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
       # return wrapper

      # return button_grid
    def create_footer_buttons(self):
        footer_widget = QWidget()
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(10, 10, 10, 10)

        # Spacer to push everything to the right
        footer_layout.addStretch()

        # Buttons added after stretch = they go to the right
        button_names = ["Upload", "Help", "About", "Settings"]
        for name in button_names:
            button = QPushButton(name)
            button.setFixedSize(90, 30)
            button.setProperty("class", "footer-button")
            footer_layout.addWidget(button)

        footer_widget.setLayout(footer_layout)
        return footer_widget

    
    def load_section(self, name):
        print(f"[INFO] Loading section: {name}")
        if not hasattr(self, 'section_pages'):
            self.section_pages = {}

        if name not in self.section_pages:
            page = load_pages(name, self.back_to_main_menu)
            self.section_pages[name] = page
            self.stack.addWidget(page)

        self.stack.setCurrentWidget(self.section_pages[name])


    def back_to_main_menu(self):
        self.stack.setCurrentWidget(self.menu_widget)

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
