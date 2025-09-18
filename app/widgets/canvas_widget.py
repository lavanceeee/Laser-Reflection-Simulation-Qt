from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor

class CanvasWidget(QWidget):
    def __init__(self):
        super().__init__()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(240, 240, 240))



    

