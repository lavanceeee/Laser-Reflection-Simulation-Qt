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

        self.canvas = CanvasWidget()
        layout.addWidget(self.canvas, 3)

        self.control_panel = ControlPanel()
        layout.addWidget(self.control_panel, 1)

    # signal
    def _connect_signals(self):
        self.control_panel.beam_radius_changed.connect(self._on_beam_radius_changed)
        self.control_panel.depth_ratio_changed.connect(self._on_depth_ratio_changed)
        self.control_panel.laser_position_changed.connect(self._on_laser_position_changed)

    def _on_beam_radius_changed(self, value):

        print(f"激光半径变为: {value}")

    def _on_depth_ratio_changed(self, value):

        print(f"深径比变为: {value}")

    def _on_laser_position_changed(self, value):

        print(f"激光位置变为: {value}")




