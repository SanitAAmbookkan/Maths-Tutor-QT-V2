# Accessibility/accessibility.py
from PyQt5.QtCore import QCoreApplication

def set_accessibility(widget,name, description_key):
   # tr = QCoreApplication.translate
    widget.setAccessibleName(name)
    widget.setAccessibleDescription(description_key)