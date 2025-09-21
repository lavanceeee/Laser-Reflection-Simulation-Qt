from PyQt6.QtGui import QPen, QColor, QPainterPath
from PyQt6.QtCore import QPointF
from app.algorithm.points_equation import GaussianEquation

class StaticRender:
    def render_scene(self, painter, width, height, scene_model):
        
        self._draw_gaussian_hole(painter, scene_model)

        self._draw_laser_radius(painter, scene_model)

        self._draw_laser_pos(painter, scene_model)

    # 高斯孔洞
    def _draw_gaussian_hole(self, painter, scene_model):
        
        logical_width = painter.window().width()
        logical_height = painter.window().height()

        hole_center_x = logical_width * 0.6  # 60%位置
        hole_center_y = logical_height * 0.5  # 50%位置
    
        points = GaussianEquation.calculate_gaussian_points(
            hole_center_x,
            hole_center_y,
            scene_model.laser_radius,
            scene_model.depth_ratio
        )

        #抗锯齿
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setPen(QPen(QColor(0, 0, 255), 1))

        if points:
            path = QPainterPath()
            path.moveTo(QPointF(points[0][0], points[0][1]))

            for x, y in points[1:]:
                path.lineTo(QPointF(x, y))

            painter.drawPath(path)

    def _draw_laser_radius(self, painter, scene_model):
        logical_width = painter.window().width()
        logical_height = painter.window().height()

        laser_center_x = logical_width * 0.55
        laser_center_y = logical_height * 0.5

        laser_radius = scene_model.laser_radius

        # points = LaserRadiusEquation.calcualte_laser_radius_points(
        #     laser_center_x,
        #     laser_center_y,
        #     scene_model.beam_radius
        # )

        start_y = laser_center_y - laser_radius
        end_y = laser_center_y + laser_radius

        painter.setPen(QPen(QColor(255, 0, 0), 1))

        painter.drawLine(
            QPointF(laser_center_x, start_y),
            QPointF(laser_center_x, end_y)
        )

    def _draw_laser_pos(self, painter, scene_model):

        logical_width = painter.window().width()
        logical_height = painter.window().height()

        laser_center_x = logical_width * 0.55
        laser_center_y = logical_height * 0.5
        laser_radius = scene_model.laser_radius

        #将数值映射到坐标轴
        position_ratio = (scene_model.laser_position - 1) / 49  # 0-1范围
        y_offset = (position_ratio - 0.5) * 2 * laser_radius    # -radius 到 +radius
        laser_y = laser_center_y + y_offset

        #更新激光坐标
        scene_model.laser_pos = (laser_center_x, laser_y)

        # 绘制激光位置点
        painter.setPen(QPen(QColor(0, 255, 0), 0))
        painter.drawPoint(QPointF(laser_center_x, laser_y))
   