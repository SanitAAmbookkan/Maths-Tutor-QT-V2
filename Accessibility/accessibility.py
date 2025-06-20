# Accessibility/accessibility.py
from PyQt5.QtCore import QCoreApplication

def set_accessibility(widget, name_key, description_key, context="Accessibility"):
    tr = QCoreApplication.translate
    widget.setAccessibleName(tr(context, name_key))
    widget.setAccessibleDescription(tr(context, description_key))
