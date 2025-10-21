from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt, pyqtSignal
from app.core.scene_model import SceneModel
from app.render.static_render import StaticRender
from app.render.dynamic_render import DynamicRender
from app.algorithm.next_pos import NextPosition
from app.algorithm.update_laser_direction import UpdateLaser
from app.render.function_render import FunctionRender
from app.core.energy_tracker import EnergyTracker
from app.core.label_manager import LabelManager
from app.render.label_renderer import LabelRenderer
from app.utils.decorators import reset_before_update

class CanvasWidget(QWidget):
    # update table signal
    reflection_data_update_signal = pyqtSignal(dict)
    # clear table signal
    clear_table_signal = pyqtSignal()
    laser_finished_signal = pyqtSignal(object)

    def __init__(self):
        super().__init__()

        # loading default paramter
        self.scene_model = SceneModel()
        self.next_position = NextPosition()

        self.static_render = StaticRender()
        self.dynamic_render = DynamicRender()
        self.function_render = FunctionRender()
        self.energy_tracker = EnergyTracker()

        self.label_manager = LabelManager()
        self.label_renderer = LabelRenderer()

        # alert info
        self.laser_wavelength = 632
        self.refractive_index = 4.2231
        self.extinction_coefficient = 0.061005
        self.hole_radius = 25
        self.hole_depth = 50
        self.laser_radius = 25
        self.depth_ratio = 2.0

        # 缩放
        self.scale_factor = 1.0
        self.min_scale = 0.1
        self.max_scale = 50.0

        self.offset_x = 0.0
        self.offset_y = 0.0

        # 鼠标拖动状态
        self.is_dragging = False
        self.drag_start_x = 0
        self.drag_start_y = 0

    # 绘制静态画面
    def paintEvent(self, event):
        painter = QPainter(self)

        # 更新model宽高
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

        if self.dynamic_render.is_animation_complete:

            # 切线
            self.function_render.render_tangent_line(painter, self.scene_model)

            # 法线
            self.function_render.render_normal_line(painter, self.scene_model)

            self.label_renderer.render_labels(painter, self.label_manager.labels)

        # TestRender.draw_current_laser_line(painter, self.scene_model)
        painter.restore()

        self._draw_alerting_info(painter)

    def _draw_alerting_info(self, painter):
        margin_left = 10
        margin_top = 30
        line_height = 30

        alerts = [
            "光在小孔中的菲涅尔反射与能量吸收",
            f"激光波长：{self.laser_wavelength}nm",
            f"材料复折射率：{self.refractive_index:.4f} + i{self.extinction_coefficient:.6f}",
            f"孔洞半径：{self.hole_radius}μm， 孔洞深度：{self.hole_depth:.1f}μm",
            f"入射激光半径：{self.laser_radius}"
        ]

        for index, alert in enumerate(alerts):
            painter.setPen(QColor(0, 0, 0, 256))
            font = painter.font()

            if index == 0:
                font.setPointSize(15)
                font.setBold(True)
            else:
                font.setPointSize(12)
                font.setBold(False)

            painter.setFont(font)
            painter.drawText(
                margin_left,
                margin_top + index * line_height,
                alert
            )

    # window resize event
    # fix: Mismatch issue caused by window size switching during path drawing
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.scene_model.is_firing:
            self.scene_model.reset_model()
            self.label_manager.clear_labels()
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

    @reset_before_update
    def set_beam_radius(self, radius):
        self.scene_model.laser_radius = radius
        self.laser_radius = radius
        self.update()

    @reset_before_update
    def set_hole_radius(self, hole_radius):
        self.scene_model.set_hole_radius(hole_radius)
        self.hole_radius = hole_radius
        self.hole_depth = hole_radius * self.depth_ratio
        self.update()

    @reset_before_update
    def set_depth_ratio(self, ratio):
        self.scene_model.set_depth_ratio(ratio)
        self.depth_ratio = ratio
        self.hole_depth = self.hole_radius * self.depth_ratio
        self.update()

    @reset_before_update
    def set_laser_position(self, position):
        self.scene_model.laser_position = position
        self.update()

    @reset_before_update
    def start_laser_firing(self):
        start_pos = self.scene_model.laser_pos
        self.scene_model.is_firing = True
        self.scene_model.laser_path = [start_pos]

        #更新初始坐标
        self.scene_model.current_segment['path_function']['b'] = start_pos[1]

        self._calcuate_complete_path()

        self.dynamic_render.start_animation(self.update)

    @reset_before_update
    def update_laser_wavelength(self, index):
        self.laser_wavelength = index
        self.update()

    @reset_before_update
    def update_refractive_index(self, index):
        self.refractive_index = index
        self.energy_tracker.absorptivity_calculator.refractive_index = index
        self.update()

    @reset_before_update
    def update_extinction_coefficient(self, index):
        self.extinction_coefficient = index
        self.energy_tracker.absorptivity_calculator.extinction_coefficient= index
        self.update()
        
    def _calcuate_complete_path(self):
        while True:
            current_position = self.scene_model.laser_path[-1]
            result_point = self.next_position.calcuate_next_pos(current_position, self.scene_model)

            if result_point is not None:
                self.scene_model.laser_path.append(result_point)

                UpdateLaser.update_laser(self.scene_model)

                if self.scene_model.incident_angle:
                    latest_angle = self.scene_model.incident_angle[-1]
                    self.energy_tracker.calcuate_and_record(
                        self.scene_model,
                        latest_angle
                    )

                if self.scene_model.reflection_data:
                    latest_data = self.scene_model.reflection_data[-1]
                    anchor_point = self.scene_model.laser_path[-1]
                    self.label_manager.add_label(anchor_point, latest_data)

                    # self.reflection_data_update_signal.emit(latest_data)
            else:
                self._draw_exit_ray()
                # self.laser_finished_signal.emit(self.scene_model)
                print("结束")
                break

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

    # 清空显示台
    @reset_before_update
    def clear_display(self):
        # fix：更新直线为水平
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
