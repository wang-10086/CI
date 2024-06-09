import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTextEdit, QLabel, QInputDialog, QMessageBox
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush, QFont, QPalette
from PyQt5.QtCore import QTimer, Qt, QPoint


class SignalButton(QPushButton):
    def __init__(self, signalID, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.signalID = signalID
        self.is_selected = False
        self.setStyleSheet("QPushButton { color: white; background-color:black; }")
        self.setFixedSize(20, 20)

    def mousePressEvent(self, event):
        self.is_selected = not self.is_selected
        if self.is_selected:
            pass
        else:
            pass
        super().mousePressEvent(event)


class SwitchButton(QPushButton):
    def __init__(self, switchID, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.switchID = switchID
        self.is_selected = False
        self.is_blinking = False
        self.setStyleSheet("QPushButton { color: white; background-color: rgba(255, 255, 255, 0); }")
        self.setFixedSize(20, 20)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.blink)

    def mousePressEvent(self, event):
        self.is_selected = not self.is_selected
        if self.is_selected:
            self.start_blinking()
        else:
            self.stop_blinking()
        super().mousePressEvent(event)

    def start_blinking(self):
        self.timer.start(800)
        self.is_blinking = True

    def stop_blinking(self):
        self.timer.stop()
        self.is_blinking = False
        self.setStyleSheet("QPushButton { color: white; background-color: rgba(255, 255, 255, 0); }")

    def blink(self):
        if self.is_blinking:
            if self.styleSheet() == "QPushButton { color: white; background-color: rgba(255, 255, 255, 0); }":
                self.setStyleSheet("QPushButton { color: black; background-color:yellow; }")
            else:
                self.setStyleSheet("QPushButton { color: white; background-color: rgba(255, 255, 255, 0); }")
