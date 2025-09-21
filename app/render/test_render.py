from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt
import math

class TestRender:
    
    @staticmethod
    def draw_current_laser_line(painter: QPainter, scene_model):

        print("进入画画")

        """画当前激光直线 y = kx + b"""
        k = scene_model.current_segment['path_function']['k']
        b = scene_model.current_segment['path_function']['b']

        print(f"k:{k}, b:{b}")
        
        # 检查是否有效
        if k == 0 and b == 0:
            return
        if math.isnan(k) or math.isnan(b):
            return
            
        # 紫色虚线
        pen = QPen(QColor(255, 0, 255))
        pen.setWidth(2)
        painter.setPen(pen)
        
        # 简单画一条线：从x=0到x=800
        x1 = 0
        y1 = k * x1 + b
        x2 = 800
        y2 = k * x2 + b
        
        painter.drawLine(int(x1), int(y1), int(x2), int(y2))