import sys, os,shutil
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QDialog, QVBoxLayout,
    QPushButton, QComboBox, QHBoxLayout, QCheckBox, QFrame,
    QWidget, QGridLayout,QInputDialog, QFileDialog, QMessageBox,
)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy #imported to resize button
from pages.ques_functions import load_pages  # ← your new function
from question.loader import QuestionProcessor

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

        self.ok_button = QPushButton("Continue")
        self.ok_button.setDefault(True)
        self.ok_button.setAutoDefault(True)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setAutoDefault(False)
        self.cancel_button.setShortcut(Qt.Key_Escape)


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
        self.current_theme = "light"  # Initial theme


        self.difficulty_index = 1 # Default to level 0 (e.g., "Very Easy")
    def init_ui(self):
        self.central_widget = QWidget()
        self.central_widget.setProperty("class", "central-widget")
        self.central_widget.setProperty("theme", "light")
        self.main_layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        # Track current theme
        self.current_theme = "light"
        
        self.menu_widget = QWidget()
        menu_layout = QVBoxLayout()
        menu_layout.setAlignment(Qt.AlignCenter)
    
         # Top bar for theme toggle
        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(0, 0, 0, 0)

         # Theme button (🌙 for light, ☀️ for dark)
        self.theme_button = QPushButton("🌙")
        self.theme_button.setFixedSize(40, 40)
        self.theme_button.setToolTip("Toggle Light/Dark Theme")
        self.theme_button.clicked.connect(self.toggle_theme)

        top_bar.addWidget(self.theme_button, alignment=Qt.AlignLeft)
        top_bar.addStretch()

        menu_layout.addLayout(top_bar)

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
        
        menu_layout.addStretch()
        # Bottom-left audio toggle
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 0, 0)

        self.audio_button = QPushButton("🔊")
        self.audio_button.setObjectName("audio-button")
        self.audio_button.setFixedSize(50, 50)
        self.audio_button.setToolTip("Toggle Mute/Unmute")
        self.audio_button.clicked.connect(self.toggle_audio)

        bottom_layout.addWidget(self.audio_button, alignment=Qt.AlignLeft)
        bottom_layout.addStretch()

        menu_layout.addLayout(bottom_layout)

        self.menu_widget.setLayout(menu_layout)
        self.main_layout.addWidget(self.menu_widget)
        
    def toggle_audio(self):
      current = self.audio_button.text()
      self.audio_button.setText("🔇" if current == "🔊" else "🔊")
      print("Muted" if current == "🔊" else "Unmuted")


    def create_buttons(self):
        button_grid = QGridLayout()
        button_grid.setSpacing(10)
        button_grid.setContentsMargins(10, 10, 10, 10)

        sections = ["Story", "Time", "Currency", "Distance", "Bellring", "Operations", "Upload"]
        self.menu_buttons = [] 
        
        for i, name in enumerate(sections):
            button = QPushButton(name)

            # Set a good preferred base size
            button.setMinimumSize(160, 50)
            button.setMaximumSize(220, 60)  # Optional: Prevent growing too big

             # Use Preferred policy to allow controlled resizing
            button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

            button.setProperty("class", "menu-button")
            button.clicked.connect(lambda checked, n=name: self.load_section(n))

            self.menu_buttons.append(button)

            row, col = divmod(i, 3)
            button_grid.addWidget(button, row, col)
 
        # Settings button
        settings_button = QPushButton("Settings")
        settings_button.setFixedSize(150, 40)
        settings_button.setProperty("class", "menu-button")
        settings_button.clicked.connect(self.open_settings)

        row, col = divmod(len(sections), 3)
        button_grid.addWidget(settings_button, row, col)


        return button_grid
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
    def load_section(self, name):
        print(f"[INFO] Loading section: {name}")
        self.menu_widget.hide()

        # First: process questions
        #self.processor = QuestionProcessor(name, self.difficulty_index)
        #self.processor.process_file()

        # ✅ Step 1: Create the page first
        page = load_pages(name, self.back_to_main_menu, self.difficulty_index,main_window=self)

        # ✅ Step 2: Now apply the theme (after page is created)
        page.setProperty("theme", self.current_theme)
        page.style().unpolish(page)
        page.style().polish(page)

        # ✅ Step 3: Clean up old section if any
        if self.main_layout.count() > 1:
            old_page = self.main_layout.takeAt(1)
            if old_page and old_page.widget():
                old_page.widget().deleteLater()

        # ✅ Step 4: Add the new page
        self.main_layout.addWidget(page)

    
    def back_to_main_menu(self):
        # Remove current section widget (not the menu itself)
        if self.main_layout.count() > 1:
            old_page = self.main_layout.takeAt(1)
            if old_page and old_page.widget():
                old_page.widget().deleteLater()
 
        self.menu_widget.show()
    def clear_main_layout(self):
        for i in reversed(range(self.main_layout.count())):
            widget = self.main_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

    
    def upload_excel_with_code(self):
        code, ok = QInputDialog.getText(self, "Access Code", "Enter Teacher Code:")
        if not ok or code != "teacher123":
            QMessageBox.critical(self, "Access Denied", "Incorrect code.")
            return

        file_path, _ = QFileDialog.getOpenFileName(self, "Select Excel File", "", "Excel Files (*.xlsx)")
        if not file_path:
            return

        try:
            # Simple validation using pandas
            import pandas as pd
            df = pd.read_excel(file_path)

            required = {"type", "input", "output"}  # Based on processor.py expectations
            if not required.issubset(df.columns):
                QMessageBox.critical(self, "Invalid File", "Excel must have columns: type, input, output")
                return

            # Save the file (overwrite old one)
            dest = os.path.join(os.getcwd(), "question", "question.xlsx")
            shutil.copyfile(file_path, dest)
            QMessageBox.information(self, "Success", "Questions uploaded successfully!")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to upload: {e}")

    def load_style(self, qss_file):
        path = os.path.join("styles", qss_file)
        if os.path.exists(path):
            with open(path, "r") as f:
                self.setStyleSheet(f.read())
        
    
    def toggle_theme(self):
       # Toggle the theme
       self.current_theme = "dark" if self.current_theme == "light" else "light"
    
       # Update theme property on central widget
       self.central_widget.setProperty("theme", self.current_theme)
    
        # Refresh style
       self.central_widget.style().unpolish(self.central_widget)
       self.central_widget.style().polish(self.central_widget)

        # Also update theme icon
       self.theme_button.setText("☀️" if self.current_theme == "dark" else "🌙")


 
   
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