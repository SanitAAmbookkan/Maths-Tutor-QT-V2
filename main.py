import sys, os,shutil
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QDialog, QVBoxLayout,
    QPushButton, QComboBox, QHBoxLayout, QCheckBox, QFrame,
    QWidget, QGridLayout,QInputDialog, QFileDialog, QMessageBox
)
from PyQt5.QtWidgets import QStackedWidget, QSizePolicy
from PyQt5.QtCore import Qt
from pages.shared_ui import create_footer_buttons 
from tempCodeRunnerFile import upload_excel_with_code
from pages.ques_functions import load_pages # ← your new function

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
     
        menu_layout.addLayout(self.create_buttons())  
        
        self.menu_widget.setLayout(menu_layout)
      
        self.stack = QStackedWidget()
        self.stack.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.stack.addWidget(self.menu_widget)

        self.main_layout.addWidget(self.stack)

        self.main_footer = self.create_main_footer_buttons()
        self.section_footer = self.create_section_footer()
        self.main_layout.addWidget(self.main_footer)
        self.main_layout.addWidget(self.section_footer)
        self.section_footer.hide()  # Hide section footer initially

        

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

    def create_main_footer_buttons(self):
        return create_footer_buttons(
            ["Upload", "Help", "About", "Settings"],
            callbacks={"Upload": self.handle_upload}
        )
    
    def create_section_footer(self):
        return create_footer_buttons(["Help", "About", "Settings"])


    def load_section(self, name):
        print(f"[INFO] Loading section: {name}")

        if not hasattr(self, 'section_pages'):
            self.section_pages = {}

        if name not in self.section_pages:
            page = load_pages(name, self.back_to_main_menu)
            self.section_pages[name] = page
            self.stack.addWidget(page)

        self.stack.setCurrentWidget(self.section_pages[name])
        self.main_footer.hide()
        self.section_footer.show()


    def back_to_main_menu(self):
        self.stack.setCurrentWidget(self.menu_widget)
        self.menu_widget.show()
        self.section_footer.hide()
        self.main_footer.show()

    
    def handle_upload(self):
        upload_excel_with_code(self)

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
