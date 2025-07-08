from PyQt5.QtCore import QThread, pyqtSignal, QObject
import pyttsx3

class TTSWorker(QThread):
    finished = pyqtSignal()

    def __init__(self, text):
        super().__init__()
        self.text = text
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1.0)

    def run(self):
        self.engine.say(self.text)
        self.engine.runAndWait()
        self.finished.emit()

class TextToSpeech(QObject):
    def __init__(self):
        super().__init__()
        self.thread = None

    def speak(self, text):
        if self.thread and self.thread.isRunning():
            self.thread.terminate()
            self.thread.wait()

        self.thread = TTSWorker(text)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()
