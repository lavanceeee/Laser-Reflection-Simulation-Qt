from PyQt6.QtGui import QPainter, QFont, QColor, QBrush, QPen
from PyQt6.QtCore import Qt, QRectF

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
        
        font_metrics = painter.fontMetrics()
        line_height = font_metrics.height()

        combined_text = " ".join(text_lines)
        painter.drawText(x, y, combined_text)
        
        # # 逐行绘制文字
        # for i, line in enumerate(text_lines):
        #     text_y = y + (i + 1) * line_height  # +1 是因为文字基线位置
        #     painter.drawText(x, text_y, line)