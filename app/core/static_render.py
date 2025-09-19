from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QColor, QPen, QPainterPath
from app.algorithm.gaussian_hole_equation import GaussianEquation

class StaticRender:
    def render_scene(self, painter, width, height, scene_model):
        
        self._draw_gaussian_hole(painter, scene_model)

        # self._draw_laser_source(painter, scene_model)


    def _draw_gaussian_hole(self, painter, scene_model):
        
        logical_width = painter.window().width()
        logical_height = painter.window().height()

        hole_center_x = logical_width * scene_model.hole_center_ratio[0]  # 60%位置
        hole_center_y = logical_height * scene_model.hole_center_ratio[1]  # 50%位置
    
        points = GaussianEquation.calculate_gaussian_points(
            hole_center_x,
            hole_center_y,
            scene_model.beam_radius,
            scene_model.depth_ratio
        )

        #抗锯齿
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setPen(QPen(QColor(0, 0, 255), 2))

        if points:
            path = QPainterPath()
            path.moveTo(QPointF(points[0][0], points[0][1]))

            for x, y in points[1:]:
                path.lineTo(QPointF(x, y))

            painter.drawPath(path)


         