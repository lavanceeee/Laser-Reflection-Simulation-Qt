from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtGui import QIcon
from app.widgets.canvas_widget import CanvasWidget
from app.widgets.control_panel import ControlPanel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._set_window()
        self._setup_layout()
        self._connect_signals()

    def _set_window(self):
        self.setWindowTitle("光在小孔中的菲涅尔反射与能量吸收")
        self.setGeometry(100, 100, 800, 600)

        self.setWindowIcon(QIcon('app-icon.png'))

    def _setup_layout(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # canvas
        self.canvas = CanvasWidget()
        layout.addWidget(self.canvas, 3)

        # panel
        self.control_panel = ControlPanel()
        layout.addWidget(self.control_panel, 1)

    # signal
    def _connect_signals(self):
        self.control_panel.beam_radius_changed.connect(self._on_beam_radius_changed)
        self.control_panel.depth_ratio_changed.connect(self._on_depth_ratio_changed)

        # 孔洞半径变化
        self.control_panel.hole_radius_changed.connect(self._on_hole_radius_changed)
        self.control_panel.laser_position_changed.connect(self._on_laser_position_changed)

        self.control_panel.laser_fire_started.connect(self._on_laser_fire_started)

        # 清空显示台
        self.control_panel.clear_display.connect(self._on_clear_display)

        # 实部 虚部两个参数
        self.control_panel.laser_refractive_index_changed_in_panel.connect(self._laser_refractive_index_changed)
        self.control_panel.laser_extinction_coefficient_changed_in_panel.connect(self._laser_extinction_coeffic)
        self.control_panel.laser_wavelength_changed_in_panel.connect(self._laser_wavelength_changed)

        # 更新table信号
        self.canvas.reflection_data_update_signal.connect(self.control_panel.add_reflection_data)

        self.canvas.clear_table_signal.connect(self.control_panel.clear_table)

        self.canvas.laser_finished_signal.connect(
            self._on_laser_finished
        )
   
    # signal
    def _on_beam_radius_changed(self, radius):
        self.canvas.set_beam_radius(radius)

    def _on_depth_ratio_changed(self, ratio):
        self.canvas.set_depth_ratio(ratio)

    def _on_hole_radius_changed(self, radius):
        self.canvas.set_hole_radius(radius)

    def _on_laser_position_changed(self, position):
        self.canvas.set_laser_position(position)

    def _on_laser_fire_started(self):
        self.canvas.start_laser_firing()

    def _on_clear_display(self):
        self.canvas.clear_display()
    
    def _on_laser_finished(self, scene_model):
        self.control_panel.clear_table()

        for reflection_data in scene_model.reflection_data:
            self.control_panel.add_reflection_data(reflection_data)

        self.control_panel.update_total_absorptivity(scene_model)

    def _laser_refractive_index_changed(self, index):
        self.canvas.update_refractive_index(index=index)

    def _laser_extinction_coeffic(self, index):
        self.canvas.update_extinction_coefficient(index=index)

    def _laser_wavelength_changed(self, index):
        self.canvas.update_laser_wavelength(index)



