# tts_module.py
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from .tts_engine import engine  # Shared engine instance

class TTSWorker(QThread):
    finished = pyqtSignal()

    def __init__(self, text):
        super().__init__()
        self.text = text
        self._is_running = True

    def run(self):
        if self._is_running:
            engine.say(self.text)
            engine.runAndWait()
        self.finished.emit()

    def stop(self):
        self._is_running = False
        engine.stop()


class TextToSpeech(QObject):
    def __init__(self):
        super().__init__()
        self.thread = None

    def speak(self, text):
        # Stop previous TTS if running
        if self.thread and self.thread.isRunning():
            self.thread.stop()
            self.thread.wait()
            self.thread.deleteLater()
            self.thread = None

        # Create new worker
        self.thread = TTSWorker(text)
        self.thread.finished.connect(self.cleanup)
        self.thread.start()

    def cleanup(self):
        if self.thread:
            self.thread.deleteLater()
            self.thread = None
