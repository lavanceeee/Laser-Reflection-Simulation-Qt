from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QColor, QPen

class FunctionRender:
    
    def render_tangent_line(self, painter, scene_model):
        """绘制所有点的切线"""
        if not scene_model.laser_path or not scene_model.tangent_slopes:
            return
            
        # 绘制所有点的切线
        for i, point in enumerate(scene_model.laser_path):

            if i == 0:
                continue

            # 确保有对应的斜率数据 (laser_path[i]对应tangent_slopes[i-1])
            if (i-1) >= len(scene_model.tangent_slopes):
                break
                
            point_x, point_y = point
            k = scene_model.tangent_slopes[i-1]  # 修正索引
            
            # 绘制切线（长度50像素）
            line_length = 5
            dx = line_length
            dy = k * dx
            
            start_x = point_x - dx
            start_y = point_y - dy
            end_x = point_x + dx  
            end_y = point_y + dy
            
            painter.setPen(QPen(QColor(0, 0, 0), 0))  # 黄色切线
            painter.drawLine(QPointF(start_x, start_y), QPointF(end_x, end_y))
    
    def render_normal_line(self, painter, scene_model):
        """绘制所有点的法线"""
        if not scene_model.laser_path or not scene_model.tangent_slopes:
            return
            
        # 绘制所有点的法线
        for i, point in enumerate(scene_model.laser_path):

            if i == 0:
                continue

            # 确保有对应的斜率数据
            if (i-1) >= len(scene_model.tangent_slopes):
                break
                
            point_x, point_y = point
            tangent_k = scene_model.tangent_slopes[i-1]
            
            # 计算法线斜率（垂直于切线）
            if abs(tangent_k) < 1e-10:
                # 切线水平，法线垂直
                normal_k = float('inf')
                # 绘制垂直法线
                line_length = 5
                start_x = point_x
                end_x = point_x
                start_y = point_y - line_length
                end_y = point_y + line_length
            else:
                # 法线斜率 = -1/切线斜率
                normal_k = -1 / tangent_k
                line_length = 10
                dx = line_length
                dy = normal_k * dx
                
                start_x = point_x - dx
                start_y = point_y - dy
                end_x = point_x + dx  
                end_y = point_y + dy
            
            painter.setPen(QPen(QColor(0, 0, 0), 0))  # 红色法线
            painter.drawLine(QPointF(start_x, start_y), QPointF(end_x, end_y))