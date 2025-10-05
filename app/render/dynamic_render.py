from PyQt6.QtCore import QPointF, QRectF, QTimeLine
from PyQt6.QtGui import QColor, QPainterPath, QPen
import math

class DynamicRender:
    def __init__(self):
        self.timeline = QTimeLine(1000)  # 2秒动画
        self.timeline.setFrameRange(0, 100)
        self.animation_progress = 1.0

    def render_laser_firing(self, painter, scene_model):
        if not scene_model.is_firing or not scene_model.laser_pos:
            return

        painter.setRenderHint(painter.RenderHint.Antialiasing, True)

        if len(scene_model.laser_path) >= 2:
            self._draw_laser_beam(painter, scene_model)
            
            # draw last point
            self._draw_latest_point(painter, scene_model)

    def _draw_laser_beam(self, painter, scene_model):
        points = scene_model.laser_path
        
        if len(points) < 2:
            return
        
        # 按路径长度而不是点数量来控制动画
        total_length = self._calculate_total_path_length(points)
        target_length = total_length * self.animation_progress
        
        # 生成动画路径
        animated_path = self._generate_animated_path(points, target_length)
        
        if len(animated_path) < 2:
            return

        # 绘制路径
        path = QPainterPath()
        first_point = animated_path[0]
        path.moveTo(QPointF(first_point[0], first_point[1]))

        for point in animated_path[1:]:
            path.lineTo(QPointF(point[0], point[1]))

        pen = QPen(QColor(101, 184, 105), 1)
        painter.setPen(pen)
        painter.drawPath(path)

    def _calculate_total_path_length(self, points):
        """计算路径总长度"""
        total_length = 0
        for i in range(1, len(points)):
            dx = points[i][0] - points[i-1][0]
            dy = points[i][1] - points[i-1][1]
            total_length += math.sqrt(dx*dx + dy*dy)
        return total_length
    
    def _generate_animated_path(self, points, target_length):
        """生成动画路径：从起点开始，沿路径绘制指定长度"""
        if target_length <= 0:
            return points[:1]  # 只返回起点
            
        animated_path = [points[0]]  # 起点
        current_length = 0
        
        for i in range(1, len(points)):
            # 计算当前段的长度
            dx = points[i][0] - points[i-1][0]
            dy = points[i][1] - points[i-1][1]
            segment_length = math.sqrt(dx*dx + dy*dy)
            
            if current_length + segment_length <= target_length:
                # 整个段都在目标长度内，添加整个点
                animated_path.append(points[i])
                current_length += segment_length
            else:
                # 段的一部分在目标长度内，计算中间点
                remaining_length = target_length - current_length
                ratio = remaining_length / segment_length
                
                # 插值计算中间点
                intermediate_x = points[i-1][0] + dx * ratio
                intermediate_y = points[i-1][1] + dy * ratio
                animated_path.append((intermediate_x, intermediate_y))
                break
                
        return animated_path
    
    def start_animation(self, update_callback):
        """开始动画"""
        self.animation_progress = 0.0
        # 断开之前的连接
        try:
            self.timeline.frameChanged.disconnect()
        except:
            pass
        self.timeline.frameChanged.connect(lambda frame: self._update_progress(frame, update_callback))
        self.timeline.start()

    def _update_progress(self, frame, update_callback):
        """更新动画进度"""
        self.animation_progress = frame / 100.0
        update_callback()  # 触发重绘

    def _draw_latest_point(self, painter, scene_model):
        painter.setPen(QPen(QColor(255, 255, 0), 1))
        painter.setBrush(QColor(0, 100, 255))
    
        point_radius = 0.1
        
        for point in scene_model.laser_path:
            point_x, point_y = point
        
            rect = QRectF(point_x - point_radius, point_y - point_radius, 
                        point_radius * 2, point_radius * 2)
            painter.drawEllipse(rect)