from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from app.widgets.canvas_widget import CanvasWidget
from app.widgets.control_panel import ControlPanel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._set_window()
        self._setup_layout()
        self._connect_signals()

    def _set_window(self):
        self.setWindowTitle("激光路径模拟")
        self.setGeometry(100, 100, 800, 600)

    def _setup_layout(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        #canvas
        self.canvas = CanvasWidget()
        layout.addWidget(self.canvas, 3)

        #panel
        self.control_panel = ControlPanel()
        layout.addWidget(self.control_panel, 1)

    # signal
    def _connect_signals(self):
        self.control_panel.beam_radius_changed.connect(self._on_beam_radius_changed)
        self.control_panel.depth_ratio_changed.connect(self._on_depth_ratio_changed)
        self.control_panel.laser_position_changed.connect(self._on_laser_position_changed)

        self.control_panel.laser_fire_started.connect(self._on_laser_fire_started)

        #清空显示台
        self.control_panel.clear_display.connect(self._on_clear_display)
        

    def _on_beam_radius_changed(self, radius):
        self.canvas.set_beam_radius(radius)

    def _on_depth_ratio_changed(self, ratio):

        self.canvas.set_depth_ratio(ratio)



    #关键的地方
    def _on_laser_position_changed(self, position):

        self.canvas.set_laser_position(position)

    def _on_laser_fire_started(self):


        self.canvas.start_laser_firing()

    def _on_clear_display(self):

        self.canvas.clear_display()




