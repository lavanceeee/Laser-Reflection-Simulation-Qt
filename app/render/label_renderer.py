from PyQt6.QtGui import QFont, QColor


class LabelRenderer:
    def __init__(self):
        self.font = QFont("Arial", 2) 
        self.padding = 1
        self.corner_radius = 1
        
    def render_labels(self, painter, labels):
        painter.setFont(self.font)
        
        for label in labels:
            x, y = label.display_position
            x = int(x)
            y = int(y)
            
            self._draw_text(painter, label.text_lines, x, y)

    def _draw_text(self, painter, text_lines, x, y):
        painter.setPen(QColor(0, 0, 0, 128)) 

        combined_text = " ".join(text_lines)
        painter.drawText(x, y, combined_text)