"""
laser_wavelength and laser refelection change widget
"""
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QDoubleSpinBox, QHBoxLayout, QLabel, QVBoxLayout, QWidget, QGroupBox, QSpinBox

class LaserParametersWidget(QWidget):
    laser_refractive_index_changed = pyqtSignal(float)
    laser_extinction_coefficient_changed = pyqtSignal(float)
    laser_wavelength_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        group_widget = QGroupBox("光与物质基本参量")
        group_widget.setStyleSheet("""
            QGroupBox {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 10px;
                margin-top: 8px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 10px;
                padding: 0 5px;
                font-weight: 500;
            }
        """)
        
        # 在分组框内创建内容布局
        content_layout = QVBoxLayout(group_widget)
        content_layout.setSpacing(5)
        
        main_layout.addWidget(group_widget)

        # 1. laser wavelength widget
        laser_wavelength_layout = QHBoxLayout()
        laser_wavelength_layout.addWidget(QLabel("激光波长："))

        # QDoubleSpinBox
        self.laser_wavelength = QSpinBox()
        self.laser_wavelength.setRange(0, 10000)
        self.laser_wavelength.setValue(632)

        laser_wavelength_layout.addWidget(self.laser_wavelength)
        laser_wavelength_layout.addWidget(QLabel("nm"))
        laser_wavelength_layout.addStretch()

        # 2. laser reflective index
        laser_refractive_index_layout = QHBoxLayout()
        laser_refractive_index_layout.addWidget(QLabel("n："))

        self.laser_reflective_index = QDoubleSpinBox()
        self.laser_reflective_index.setDecimals(4)
        self.laser_reflective_index.setSingleStep(0.0001)
        self.laser_reflective_index.setValue(4.2231)

        laser_refractive_index_layout.addWidget(self.laser_reflective_index)
        laser_refractive_index_layout.addStretch()

        # 3. laser extinction coefficient
        laser_extinction_coefficient_layout = QHBoxLayout()
        laser_extinction_coefficient_layout.addWidget(QLabel("k："))

        self.laser_extinction_coefficient = QDoubleSpinBox()
        self.laser_extinction_coefficient.setDecimals(6)
        self.laser_extinction_coefficient.setSingleStep(0.000001)
        self.laser_extinction_coefficient.setValue(0.061005)

        laser_extinction_coefficient_layout.addWidget(self.laser_extinction_coefficient)
        laser_extinction_coefficient_layout.addStretch()

        content_layout.addLayout(laser_wavelength_layout)
        content_layout.addWidget(QLabel("材料复折射率："))
        content_layout.addLayout(laser_refractive_index_layout)
        content_layout.addLayout(laser_extinction_coefficient_layout)
        
        content_layout.addStretch()

        self.laser_wavelength.valueChanged.connect(self.laser_wavelength_changed.emit)
        self.laser_reflective_index.valueChanged.connect(self.laser_refractive_index_changed.emit)
        self.laser_extinction_coefficient.valueChanged.connect(self.laser_extinction_coefficient_changed.emit)
