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
            
            # 计算文本区域的尺寸
            text_width, text_height = self._calculate_text_size(painter, label.text_lines)
            
            # 绘制圆角背景框
            self._draw_background(painter, x, y, text_width, text_height)
            
            # 绘制文字
            self._draw_text(painter, label.text_lines, x, y)
    
    def _calculate_text_size(self, painter, text_lines):
        """计算文本区域的总宽度和高度"""
        font_metrics = painter.fontMetrics()
        
        # 计算最大宽度
        max_width = 0
        for line in text_lines:
            line_width = font_metrics.horizontalAdvance(line)
            max_width = max(max_width, line_width)
        
        # 计算总高度
        line_height = font_metrics.height()
        total_height = line_height * len(text_lines)
        
        return max_width, total_height
    
    def _draw_background(self, painter, x, y, text_width, text_height):
        """绘制淡蓝色圆角背景框"""
        # 设置背景色和边框
        background_color = QColor(173, 216, 230, 200)  # 淡蓝色，半透明
        border_color = QColor(100, 149, 237, 150)      # 深一点的蓝色边框
        
        painter.setBrush(QBrush(background_color))
        painter.setPen(QPen(border_color, 1))
        
        # 计算背景框的位置和尺寸（加上内边距）
        bg_x = x - self.padding
        bg_y = y - self.padding
        bg_width = text_width + 2 * self.padding
        bg_height = text_height + 2 * self.padding
        
        # 绘制圆角矩形
        background_rect = QRectF(bg_x, bg_y, bg_width, bg_height)
        painter.drawRoundedRect(background_rect, self.corner_radius, self.corner_radius)
    
    def _draw_text(self, painter, text_lines, x, y):
        """绘制文字"""
        # 设置文字颜色
        painter.setPen(QColor(50, 50, 50))  # 深灰色文字，更好的对比度
        
        font_metrics = painter.fontMetrics()
        line_height = font_metrics.height()
        
        # 逐行绘制文字
        for i, line in enumerate(text_lines):
            text_y = y + (i + 1) * line_height  # +1 是因为文字基线位置
            painter.drawText(x, text_y, line)