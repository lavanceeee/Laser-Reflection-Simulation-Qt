from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor
from app.core.scene_model import SceneModel
from app.core.static_render import StaticRender

class CanvasWidget(QWidget):
    def __init__(self):
        super().__init__()

        #loading default paramter
        self.scene_model = SceneModel()

        self.static_render = StaticRender()

        #缩放
        self.scale_factor = 1.0
        self.min_scale = 0.1
        self.max_scale = 5.0

        self.offset_x = 0.0
        self.offset_y = 0.0

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.fillRect(self.rect(), QColor(240, 240, 240))
    
        # 2. 保存当前状态
        painter.save()

        painter.translate(self.offset_x, self.offset_y)
        painter.scale(self.scale_factor, self.scale_factor)

        self.static_render.render_scene(
            painter,
            int(self.width() / self.scale_factor),
            int(self.height() / self.scale_factor),
            self.scene_model
        )

        painter.restore()

    #鼠标缩放事件
    def wheelEvent(self, event):

        mouse_pos = event.position()
        mouse_x = mouse_pos.x()
        mouse_y = mouse_pos.y()
        
        delta = event.angleDelta().y()

        zoom_in = delta > 0
        zoom_factor = 1.1 if zoom_in else 1 / 1.1

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

    def set_beam_radius(self, radius):
        self.beam_radius = radius
        self.update()

    def set_depth_ratio(self, ratio):
        self.depth_ratio = ratio
        self.update()

    def set_laser_position(self, position):
        self.laser_position = position
        self.update()

    

    

    

