import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QDialog, 
                            QVBoxLayout, QPushButton, QComboBox, QHBoxLayout,
                            QCheckBox, QFrame, QWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class RootWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Maths Tutor - Language Selection")
        self.setFixedSize(400, 250)
        
        # Initialize UI
        self.init_ui()
        
        # Load style
        self.load_style("language_dialog.css")
    
    def init_ui(self):
        # Create widgets
        title_label = QLabel("Welcome to Maths Tutor!")
        title_label.setProperty("class", "title")
        
        language_label = QLabel("Select your preferred language:")
        language_label.setProperty("class", "subtitle")
        
        self.language_combo = QComboBox()
        self.language_combo.addItems(["English", "Español", "Français", "Deutsch", "中文"])
        self.language_combo.setProperty("class", "combo-box")
        
        self.remember_check = QCheckBox("Remember my selection")
        self.remember_check.setProperty("class", "checkbox")
        self.remember_check.setChecked(True)
        
        # Buttons
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setProperty("class", "danger-button")
        self.ok_button = QPushButton("Continue")
        self.ok_button.setProperty("class", "primary-button")
        
        # Layout
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
        
        # Connections
        self.cancel_button.clicked.connect(self.reject)
        self.ok_button.clicked.connect(self.accept)
    
    def create_horizontal_line(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        return line
    
    def load_style(self, css_file):
        """Load styles from external CSS file"""
        style_path = os.path.join("styles", css_file)
        if os.path.exists(style_path):
            with open(style_path, "r") as f:
                self.setStyleSheet(f.read())

class MainWindow(QMainWindow):
    def __init__(self, language="English"):
        super().__init__()
        self.setWindowTitle(f"Maths Tutor - {language}")
        self.setFixedSize(800, 500)
        
        # Initialize UI
        self.init_ui(language)
        
        # Load style
        self.load_style("main_window.css")
    
    def init_ui(self, language):
        # Central widget
        central_widget = QWidget()
        central_widget.setProperty("class", "central-widget")
        layout = QVBoxLayout(central_widget)
        
        title = QLabel("Welcome to Maths Tutor!")
        title.setProperty("class", "main-title")
        
        subtitle = QLabel(f"Ready to learn in {language}!")
        subtitle.setProperty("class", "subtitle")
        
        layout.addStretch()
        layout.addWidget(title, 0, Qt.AlignCenter)
        layout.addWidget(subtitle, 0, Qt.AlignCenter)
        layout.addStretch()
        
        self.setCentralWidget(central_widget)
    
    def load_style(self, css_file):
        """Load styles from external CSS file"""
        style_path = os.path.join("styles", css_file)
        if os.path.exists(style_path):
            with open(style_path, "r") as f:
                self.setStyleSheet(f.read())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application style
    app_style_path = os.path.join("styles", "app.css")
    if os.path.exists(app_style_path):
        with open(app_style_path, "r") as f:
            app.setStyleSheet(f.read())
    
    root_window = RootWindow()
    if root_window.exec_() == QDialog.Accepted:
        main_window = MainWindow(root_window.language_combo.currentText())
        main_window.show()
        sys.exit(app.exec_())