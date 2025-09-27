from PyQt6.QtGui import QPen, QColor, QPainterPath
from PyQt6.QtCore import QRectF, QPointF
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
        hole_center_y = logical_height * 0.5 - scene_model.mu # 50%位置
    
        points = GaussianEquation.calculate_gaussian_points(
            hole_center_x,
            hole_center_y,
            scene_model
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

    # 绘制半径
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

        painter.setPen(QPen(QColor(0, 0, 0), 0))  # 灰色

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
        laser_y = laser_center_y - laser_radius + scene_model.laser_position

        #更新激光坐标
        scene_model.laser_pos = (laser_center_x, laser_y)

        # 绘制激光位置点
        painter.setPen(QPen(QColor(255, 0, 0), 0))
        painter.setBrush(QColor(255, 0, 0))

        inner_radius = 0.2
        inner_rect = QRectF(laser_center_x - inner_radius, laser_y - inner_radius,
                            inner_radius * 2, inner_radius * 2)

        painter.drawEllipse(inner_rect)

        # 重置brush，透明
        painter.setBrush(QColor(0, 0, 0, 0))

        #激光样式
        self._draw_laser_device(painter, laser_center_x, laser_y)

    def _draw_laser_device(self, painter, center_x, center_y):
        """绘制激光器设备"""
        # 转换为整数坐标
        center_x = int(center_x)
        center_y = int(center_y)
        
        # 小正方形（出射口）- 以入射点为中心
        square_size = 4
        square_x = center_x - square_size // 2
        square_y = center_y - square_size // 2
    
        painter.setPen(QPen(QColor(100, 100, 255), 0))  # 蓝色边框
        painter.setBrush(QColor(200, 200, 255, 100))    # 浅蓝色填充
        painter.drawRect(square_x, square_y, square_size, square_size)
    
        # 长方形（激光器主体）- 在小正方形左侧
        rect_width = 20
        rect_height = 6
        rect_x = center_x - square_size // 2 - rect_width  # 紧贴小正方形左侧
        rect_y = center_y - rect_height // 2
    
        painter.setPen(QPen(QColor(100, 100, 255), 0))  # 蓝色边框
        painter.setBrush(QColor(150, 150, 255, 100))    # 稍深蓝色填充
        painter.drawRect(rect_x, rect_y, rect_width, rect_height)
        
        # 重置brush避免影响其他绘制！！！
        painter.setBrush(QColor(0, 0, 0, 0))  # 透明brush