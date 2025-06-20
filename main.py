import sys, os, shutil
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QDialog, QVBoxLayout,
    QPushButton, QComboBox, QHBoxLayout, QCheckBox, QFrame,
    QWidget, QGridLayout, QInputDialog, QFileDialog, QMessageBox,
    QSizePolicy,
)
from PyQt5.QtCore import QTranslator, Qt, QCoreApplication, QTimer
from pages.ques_functions import load_pages
from Accessibility.accessibility import set_accessibility  # Accessibility support

def tr(ctx, text):
    return QCoreApplication.translate(ctx, text)

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
        self.setWindowTitle(tr("MainWindow", "Maths Tutor - {0}").format(language))
        self.resize(900, 600)
        self.language = language
        self.init_ui()
        self.load_style("main_window.qss")
        self.current_theme = "light"

    def init_ui(self):
        self.central_widget = QWidget()
        self.central_widget.setProperty("class", "central-widget")
        self.central_widget.setProperty("theme", "light")
        self.main_layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        self.current_theme = "light"

        self.menu_widget = QWidget()
        menu_layout = QVBoxLayout()
        menu_layout.setAlignment(Qt.AlignCenter)

        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(0, 0, 0, 0)

        self.theme_button = QPushButton("🌙")
        self.theme_button.setFixedSize(40, 40)
        self.theme_button.setToolTip(tr("MainWindow", "Toggle Light/Dark Theme"))
        set_accessibility(self.theme_button,
                          name_key="Theme Toggle Button",
                          description_key="Button to toggle light or dark theme",
                          context="MainWindow")
        self.theme_button.clicked.connect(self.toggle_theme)

        top_bar.addWidget(self.theme_button, alignment=Qt.AlignLeft)
        top_bar.addStretch()

        menu_layout.addLayout(top_bar)

        title = QLabel(tr("MainWindow", "Welcome to Maths Tutor!"))
        title.setAccessibleName(tr("MainWindow", "Welcome to Maths Tutor!"))
        title.setAlignment(Qt.AlignCenter)
        title.setProperty("class", "main-title")

        subtitle = QLabel(tr("MainWindow", "Ready to learn in {0}!").format(self.language))
        subtitle.setAccessibleName(tr("MainWindow", f"Ready to learn in {self.language}!"))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setProperty("class", "subtitle")
        
        menu_layout.addWidget(title)
        menu_layout.addWidget(subtitle)
        menu_layout.addSpacing(20)
        menu_layout.addLayout(self.create_buttons())
        menu_layout.addStretch()

        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 0, 0)

        self.audio_button = QPushButton("🔊")
        self.audio_button.setObjectName("audio-button")
        self.audio_button.setFixedSize(50, 50)
        self.audio_button.setToolTip(tr("MainWindow", "Toggle Mute/Unmute"))
        set_accessibility(self.audio_button,
                          name_key="Audio Toggle Button",
                          description_key="Button to mute or unmute the audio",
                          context="MainWindow")
        self.audio_button.clicked.connect(self.toggle_audio)

        bottom_layout.addWidget(self.audio_button, alignment=Qt.AlignLeft)
        bottom_layout.addStretch()

        menu_layout.addLayout(bottom_layout)

        self.menu_widget.setLayout(menu_layout)
        self.main_layout.addWidget(self.menu_widget)

        # Add live region label for screen reader announcements
        self.a11y_live_label = QLabel("")
        self.a11y_live_label.setVisible(False)
        self.a11y_live_label.setAccessibleName("ScreenReaderAnnounce")
        self.main_layout.addWidget(self.a11y_live_label)

    def toggle_audio(self):
        current = self.audio_button.text()
        new_text = "🔇" if current == "🔊" else "🔊"
        self.audio_button.setText(new_text)
        announcement = tr("MainWindow", "Muted") if new_text == "🔇" else tr("MainWindow", "Unmuted")
        
        # Update button's accessible name/description
        self.audio_button.setAccessibleName(announcement)
        self.audio_button.setAccessibleDescription(announcement)
        
        # Update live label (must be visible to accessibility, even if off-screen)
        self.a11y_live_label.setText("")  # Clear first
        QTimer.singleShot(100, lambda: self.a11y_live_label.setText(announcement))
        # Do not immediately clear the label; let it persist for a few seconds
        QTimer.singleShot(3000, lambda: self.a11y_live_label.setText(""))



    def create_buttons(self):
        button_grid = QGridLayout()
        button_grid.setSpacing(10)
        button_grid.setContentsMargins(10, 10, 10, 10)

        sections = [
            tr("MainWindow", "Story"),
            tr("MainWindow", "Time"),
            tr("MainWindow", "Currency"),
            tr("MainWindow", "Distance"),
            tr("MainWindow", "Bellring"),
            tr("MainWindow", "Operations"),
            tr("MainWindow", "Upload"),
        ]
        self.menu_buttons = [] 

        for i, name in enumerate(sections):
            button = QPushButton(name)
            button.setMinimumSize(160, 50)
            button.setMaximumSize(220, 60)
            button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
            button.setProperty("class", "menu-button")

            set_accessibility(button,
                              name_key=f"{name} Section Button",
                              description_key=f"Button to open the {name} section",
                              context="MainWindow")

            button.clicked.connect(lambda checked, n=name: self.load_section(n))
            self.menu_buttons.append(button)

            row, col = divmod(i, 3)
            button_grid.addWidget(button, row, col)

        return button_grid

    def load_section(self, name):
        print(f"[INFO] Loading section: {name}")
        self.menu_widget.hide()
        page = load_pages(name, self.back_to_main_menu, self)
        page.setProperty("theme", self.current_theme)
        page.style().unpolish(page)
        page.style().polish(page)

        if self.main_layout.count() > 1:
            old_page = self.main_layout.takeAt(1)
            if old_page and old_page.widget():
                old_page.widget().deleteLater()

        self.main_layout.addWidget(page)

    def back_to_main_menu(self):
        if self.main_layout.count() > 1:
            old_page = self.main_layout.takeAt(1)
            if old_page and old_page.widget():
                old_page.widget().deleteLater()

        self.menu_widget.show()

    def upload_excel_with_code(self):
        code, ok = QInputDialog.getText(self, tr("MainWindow", "Access Code"), tr("MainWindow", "Enter Teacher Code:"))
        if not ok or code != "teacher123":
            QMessageBox.critical(self, tr("MainWindow", "Access Denied"), tr("MainWindow", "Incorrect code."))
            return

        file_path, _ = QFileDialog.getOpenFileName(self, tr("MainWindow", "Select Excel File"), "", "Excel Files (*.xlsx)")
        if not file_path:
            return

        try:
            import pandas as pd
            df = pd.read_excel(file_path)
            required = {"type", "input", "output"}
            if not required.issubset(df.columns):
                QMessageBox.critical(self, tr("MainWindow", "Invalid File"), tr("MainWindow", "Excel must have columns: type, input, output"))
                return

            dest = os.path.join(os.getcwd(), "question", "question.xlsx")
            shutil.copyfile(file_path, dest)
            QMessageBox.information(self, tr("MainWindow", "Success"), tr("MainWindow", "Questions uploaded successfully!"))

        except Exception as e:
            QMessageBox.critical(self, tr("MainWindow", "Error"), tr("MainWindow", f"Failed to upload: {e}"))

    def load_style(self, qss_file):
        path = os.path.join("styles", qss_file)
        if os.path.exists(path):
            with open(path, "r") as f:
                self.setStyleSheet(f.read())

    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.central_widget.setProperty("theme", self.current_theme)
        self.central_widget.style().unpolish(self.central_widget)
        self.central_widget.style().polish(self.central_widget)
        self.theme_button.setText("☀️" if self.current_theme == "dark" else "🌙")

        announcement = tr("MainWindow", "Dark mode activated") if self.current_theme == "dark" else tr("MainWindow", "Light mode activated")
        self.a11y_live_label.setText("")
        QTimer.singleShot(100, lambda: self.a11y_live_label.setText(announcement))
        QTimer.singleShot(100, lambda: self.a11y_live_label.setAccessibleDescription(announcement))

if __name__ == "__main__":
    app = QApplication(sys.argv)

    style_file = os.path.join("styles", "app.qss")
    if os.path.exists(style_file):
        with open(style_file, "r") as f:
            app.setStyleSheet(f.read())

    dialog = RootWindow()
    if dialog.exec_() == QDialog.Accepted:
        chosen_language = dialog.language_combo.currentText()

        lang_map = {
            "English": "en",
            "हिंदी": "hi",
            "മലയാളം": "mal",
            "தமிழ்": "ta",
            "عربي": "ar",
            "संस्कृत": "sa",
        }

        lang_code = lang_map.get(chosen_language, "en")

        translator = QTranslator()
        translation_file = f"Localisation/{lang_code}.qm"
        if translator.load(translation_file):
            app.installTranslator(translator)
            print(f"[INFO] Loaded translation for {chosen_language}")

        window = MainWindow(language=chosen_language)
        window.show()
        sys.exit(app.exec_())
    else:
        sys.exit(0)
