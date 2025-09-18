from PyQt6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget, QSpinBox
from PyQt6.QtCore import pyqtSignal

class ControlPanel(QWidget):

    beam_radius_changed = pyqtSignal(int)
    depth_ratio_changed = pyqtSignal(int)
    laser_position_changed = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.setStyleSheet("border: 1px solid red;")
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        #激光半径
        beam_layout = QHBoxLayout()
        beam_layout.addWidget(QLabel("激光半径："))
        self.beam_radius = QSpinBox()
        self.beam_radius.setValue(25)
        self.beam_radius.valueChanged.connect(self.beam_radius_changed.emit)
        beam_layout.addWidget(self.beam_radius)
        # addStretch()
        beam_layout.addStretch() 
        layout.addLayout(beam_layout)

        #深径比
        depth_layout = QHBoxLayout()
        depth_layout.addWidget(QLabel("深径比："))
        self.depth_ratio = QSpinBox()
        self.depth_ratio.setValue(2)
        self.depth_ratio.valueChanged.connect(self.depth_ratio_changed.emit)
        depth_layout.addWidget(self.depth_ratio)
        depth_layout.addStretch()
        layout.addLayout(depth_layout)

        #激光入射坐标
        position_layout = QHBoxLayout()
        position_layout.addWidget(QLabel("入射坐标："))

        self.laser_pos = QSpinBox()
        self.laser_pos.setValue(25)
        self.laser_pos.valueChanged.connect(self.laser_position_changed.emit)
        position_layout.addWidget(self.laser_pos)
        position_layout.addStretch()
        layout.addLayout(position_layout)