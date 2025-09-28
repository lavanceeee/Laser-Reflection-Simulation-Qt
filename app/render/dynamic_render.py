from PyQt6.QtCore import QPointF, QRectF
from PyQt6.QtGui import QColor, QPainterPath, QPen

class DynamicRender:
    def render_laser_firing(self, painter, scene_model):
        if not scene_model.is_firing or not scene_model.laser_pos:
            return

        # anti aliasing
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)

        if len(scene_model.laser_path) >= 2:
            self._draw_laser_beam(painter, scene_model)
            
            # draw last point
            self._draw_latest_point(painter, scene_model)

    def _draw_laser_beam(self, painter, scene_model):
        points = scene_model.laser_path

        path = QPainterPath()

        first_point = points[0]
        path.moveTo(QPointF(first_point[0], first_point[1]))

        for point in points[1:]:
            path.lineTo(QPointF(point[0], point[1]))

        pen = QPen(QColor(255, 0, 0), 1)

        painter.setPen(pen)
        painter.drawPath(path)

    def _draw_latest_point(self, painter, scene_model):
        painter.setPen(QPen(QColor(255, 255, 0), 1))  # 蓝色，无边框
        painter.setBrush(QColor(0, 100, 255))  # 蓝色填充
    
        point_radius = 0.1  # 更小的半径
        
        for point in scene_model.laser_path:
            point_x, point_y = point
        
            # 绘制小圆点
            rect = QRectF(point_x - point_radius, point_y - point_radius, 
                        point_radius * 2, point_radius * 2)
            painter.drawEllipse(rect)