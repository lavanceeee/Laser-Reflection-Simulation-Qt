from PyQt6.QtGui import QPen, QColor, QPainterPath
from PyQt6.QtCore import QRectF, QPointF
from app.algorithm.points_equation import GaussianEquation

class StaticRender:
    def render_scene(self, painter, width, height, scene_model):

        #background grid
        self._draw_background_grid(painter)
        
        self._draw_gaussian_hole(painter, scene_model)

        self._draw_laser_radius(painter, scene_model)

        self._draw_laser_pos(painter, scene_model)

    def _draw_background_grid(self, painter):
        logical_width = painter.window().width()
        logical_height = painter.window().height()

        # 获取当前变换矩阵
        transform = painter.transform()
        scale = transform.m11()  # 获取缩放因子
        
        # 计算可视区域在逻辑坐标系中的范围
        inverse_transform = transform.inverted()[0]
        top_left = inverse_transform.map(QPointF(0, 0))
        bottom_right = inverse_transform.map(QPointF(logical_width, logical_height))
        
        # 扩展绘制范围
        margin = max(logical_width, logical_height) / scale
        start_x = top_left.x() - margin
        start_y = top_left.y() - margin
        end_x = bottom_right.x() + margin
        end_y = bottom_right.y() + margin
        
        # 填充扩展背景
        painter.fillRect(QRectF(start_x, start_y, end_x - start_x, end_y - start_y), QColor(248, 248, 248))

        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setPen(QPen(QColor(181, 181, 181), 0.5 / scale))  # 根据缩放调整线宽
        
        grid_spacing = 5

        # 修正的对齐计算 - 使用floor确保正确对齐
        import math
        grid_start_x = math.floor(start_x / grid_spacing) * grid_spacing
        grid_start_y = math.floor(start_y / grid_spacing) * grid_spacing

        # 绘制垂直网格线
        x = grid_start_x
        while x <= end_x:
            painter.drawLine(QPointF(x, start_y), QPointF(x, end_y))
            x += grid_spacing

        # 绘制水平网格线
        y = grid_start_y
        while y <= end_y:
            painter.drawLine(QPointF(start_x, y), QPointF(end_x, y))
            y += grid_spacing

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
        # 转换为整数坐标
        center_x = int(center_x)
        center_y = int(center_y)
        
        # 小正方形（出射口）- 以入射点为中心
        square_size = 2
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