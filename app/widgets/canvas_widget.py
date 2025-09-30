from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt
from app.core import scene_model
from app.core.scene_model import SceneModel
from app.render.static_render import StaticRender
from app.render.dynamic_render import DynamicRender
from app.algorithm.next_pos import NextPosition
from app.algorithm.update_laser_direction import UpdateLaser
from app.render.function_render import FunctionRender

class CanvasWidget(QWidget):
    def __init__(self):
        super().__init__()

        #loading default paramter
        self.scene_model = SceneModel()
        self.next_position = NextPosition()

        self.static_render = StaticRender()
        self.dynamic_render = DynamicRender()
        self.function_render = FunctionRender()

        #缩放
        self.scale_factor = 1.0
        self.min_scale = 0.1
        self.max_scale = 50.0

        self.offset_x = 0.0
        self.offset_y = 0.0
        
        # 鼠标拖动状态
        self.is_dragging = False
        self.drag_start_x = 0
        self.drag_start_y = 0

    #绘制静态画面
    def paintEvent(self, event):
        painter = QPainter(self)

        #更新model宽高
        self.scene_model.canvas_width = painter.window().width()
        self.scene_model.canvas_height = painter.window().height()

        painter.fillRect(self.rect(), QColor(240, 240, 240))
    
        # 2. 保存当前状态
        painter.save()

        painter.translate(self.offset_x, self.offset_y)
        painter.scale(self.scale_factor, self.scale_factor)

        self.static_render.render_scene(
            painter,
            painter.window().width(),
            painter.window().height(),
            self.scene_model
        )

        self.dynamic_render.render_laser_firing(painter, self.scene_model)

        # 切线
        self.function_render.render_tangent_line(painter, self.scene_model)
        
        # 法线
        self.function_render.render_normal_line(painter, self.scene_model)

        # 添加到 paintEvent 的最后
        # TestRender.draw_current_laser_line(painter, self.scene_model)
        painter.restore()

    # window resize event
    # fix(currently): Mismatch issue caused by window size switching during path drawing   
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.scene_model.is_firing:
            self.scene_model.reset_model()
            self.update()

    # 鼠标缩放事件
    def wheelEvent(self, event):

        mouse_pos = event.position()
        mouse_x = mouse_pos.x()
        mouse_y = mouse_pos.y()
        
        delta = event.angleDelta().y()

        zoom_in = delta > 0
        zoom_factor = 1.3 if zoom_in else 1 / 1.3

        new_scale = self.scale_factor * zoom_factor

        if self.min_scale <= new_scale <= self.max_scale:
            # 计算鼠标在变换后坐标系中的位置
            old_pos_x = (mouse_x - self.offset_x) / self.scale_factor
            old_pos_y = (mouse_y - self.offset_y) / self.scale_factor
            
            self.scale_factor = new_scale

            # 计算新的偏移，保持鼠标位置不变
            self.offset_x = mouse_x - old_pos_x * self.scale_factor
            self.offset_y = mouse_y - old_pos_y * self.scale_factor
            
            self.update() 

    # 鼠标拖动功能
    def mousePressEvent(self, event):
        """鼠标按下开始拖动"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = True
            self.drag_start_x = event.position().x()
            self.drag_start_y = event.position().y()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)

    def mouseMoveEvent(self, event):
        """鼠标移动拖动画布"""
        if self.is_dragging:
            # 计算移动距离
            dx = event.position().x() - self.drag_start_x
            dy = event.position().y() - self.drag_start_y
            
            # 更新偏移量
            self.offset_x += dx
            self.offset_y += dy
            
            # 更新拖动起始位置
            self.drag_start_x = event.position().x()
            self.drag_start_y = event.position().y()
            
            self.update()

    def mouseReleaseEvent(self, event):
        """鼠标释放结束拖动"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = False
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def set_beam_radius(self, radius):
        # clear path if already draw
        if self.scene_model.is_firing:
            self.scene_model.reset_model()
            self.update()
            
        self.scene_model.laser_radius = radius
        self.update()

    def set_hole_radius(self, hole_radius):
        # clear path if already draw
        if self.scene_model.is_firing:
            self.scene_model.reset_model()
            self.update()

        self.scene_model.hole_radius = hole_radius
        self.update()

    def set_depth_ratio(self, ratio):
        # clear path if already draw
        if self.scene_model.is_firing:
            self.scene_model.reset_model()
            self.update()

        self.scene_model.depth_ratio = ratio

        #坑：忘记更新A的参数
        self.scene_model.A = ratio * self.scene_model.laser_radius
        self.update()

    # update laser position
    def set_laser_position(self, position):

        # clear path if already draw
        if self.scene_model.is_firing:
            self.scene_model.reset_model()
            self.update()
            
        self.scene_model.laser_position = position
        self.update()

    def start_laser_firing(self):

        # reset model parameter
        if self.scene_model.is_firing:
            self.scene_model.reset_model()
            self.update()
        
        start_pos = self.scene_model.laser_pos
        self.scene_model.is_firing = True
        self.scene_model.laser_path = [start_pos]

        #更新初始坐标
        self.scene_model.current_segment['path_function']['b'] = start_pos[1]

        #计算交点并绘图
        self._update_laser_step()

        self.update()
    
    def _update_laser_step(self):
        if not self.scene_model.is_firing:
            return

        current_position = self.scene_model.laser_path[-1]

        result_point = self.next_position.calcuate_next_pos(current_position, self.scene_model)

        if result_point is not None:
            self.scene_model.laser_path.append(result_point)
            self.update()

            #更新segment片段信息
            UpdateLaser.update_laser(self.scene_model)

            #递归调用更新
            self._update_laser_step()
        else:
            #最后绘制一次尾函数出射
            self._draw_exit_ray()

            print("结束")

    def _draw_exit_ray(self):
        """绘制出射线"""
        last_point = self.scene_model.laser_path[-1]
        last_x, last_y = last_point
        slope = self.scene_model.current_segment['path_function']['k']
        
        if self.scene_model.current_segment['toward_right']:
            # 向右延伸
            exit_x = last_x + 60
        else:
            # 向左延伸  
            exit_x = last_x - 60
            
        exit_y = last_y + slope * (exit_x - last_x)
        self.scene_model.laser_path.append((exit_x, exit_y))
        self.update()

    #清空显示台
    def clear_display(self):
        self.scene_model.laser_path = []

        self.scene_model.tangent_slopes = []

        self.scene_model.is_firing = False

        #坑：忘记更新直线为水平了
        self.scene_model.current_segment = {
            'toward_right': True,
            'step_size': 3,
            'path_function': {
                'k': 0,          
                'b': self.scene_model.laser_pos[1]
            },
            'segment_id': 0
        }

        self.update()
