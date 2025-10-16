from PyQt6.QtWidgets import QHBoxLayout, QLabel, QTableWidget, QHeaderView, QVBoxLayout, QWidget, QSpinBox, QPushButton, QGroupBox
from PyQt6.QtCore import pyqtSignal
from app.widgets.total_absorptivity_widget import TotalAbsorptivityWidget
from app.widgets.laser_parameters import LaserParametersWidget

class ControlPanel(QWidget):
    beam_radius_changed = pyqtSignal(int)
    depth_ratio_changed = pyqtSignal(int)
    laser_position_changed = pyqtSignal(int)
    laser_fire_started = pyqtSignal()
    clear_display = pyqtSignal()
    hole_radius_changed = pyqtSignal(int)
    laser_refractive_index_changed_in_panel = pyqtSignal(float)
    laser_extinction_coefficient_changed_in_panel = pyqtSignal(float)

    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QHBoxLayout(self)
        
        # paramter selector and result area 
        left_main_widget = QWidget()
        left_main_layout = QHBoxLayout(left_main_widget)
        
        params_widget = QGroupBox("基本参数")
        params_widget.setStyleSheet("""
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
        params_layout = QVBoxLayout(params_widget)
        
        # hole_radius
        hole_radius_layout = QHBoxLayout()
        hole_radius_layout.addWidget(QLabel("孔洞半径："))
        self.hole_radius = QSpinBox()
        self.hole_radius.setValue(25)
        self.hole_radius.valueChanged.connect(self.hole_radius_changed.emit)
        self.hole_radius.valueChanged.connect(self._update_laser_pos_max)

        hole_radius_layout.addWidget(self.hole_radius)
        hole_radius_layout.addWidget(QLabel("μm"))
        
        hole_radius_layout.addStretch()
        params_layout.addLayout(hole_radius_layout)

        # depth_ratio
        depth_layout = QHBoxLayout()
        depth_layout.addWidget(QLabel("孔洞深径比："))
        self.depth_ratio = QSpinBox()
        self.depth_ratio.setValue(2)
        self.depth_ratio.valueChanged.connect(self.depth_ratio_changed.emit)
        depth_layout.addWidget(self.depth_ratio)
        depth_layout.addWidget(QLabel("(深度h/半径r)"))
        depth_layout.addStretch()
        params_layout.addLayout(depth_layout)

        # laser_radius
        beam_layout = QHBoxLayout()
        beam_layout.addWidget(QLabel("激光半径："))
        self.beam_radius = QSpinBox()
        self.beam_radius.setValue(25)
        self.beam_radius.valueChanged.connect(self.beam_radius_changed.emit)
        beam_layout.addWidget(self.beam_radius)
        beam_layout.addWidget(QLabel("μm"))
        beam_layout.addStretch() 
        params_layout.addLayout(beam_layout)
        
        # laser_position
        position_layout = QHBoxLayout()
        position_layout.addWidget(QLabel("入射坐标："))
        self.laser_pos = QSpinBox()
        self.laser_pos.setValue(25)
        self.laser_pos.setMaximum(50)

        self.laser_pos.valueChanged.connect(self.laser_position_changed.emit)
        position_layout.addWidget(self.laser_pos)
        position_layout.addStretch()
        params_layout.addLayout(position_layout)
        params_layout.addStretch()

        laser_reflection_widget = LaserParametersWidget()
        laser_reflection_widget.laser_refractive_index_changed.connect(self.laser_refractive_index_changed_in_panel)
        laser_reflection_widget.laser_extinction_coefficient_changed.connect(self.laser_extinction_coefficient_changed_in_panel)

        """
        result table 
        """
        result_widget = QWidget()
        result_layout = QVBoxLayout(result_widget)

        # create table
        self.reflection_table = QTableWidget()
        
        # line height
        self.reflection_table.setMinimumHeight(150)
        self.reflection_table.horizontalHeader().setFixedHeight(30)
        self.reflection_table.verticalHeader().setDefaultSectionSize(30)

        self.reflection_table.setColumnCount(4)
        self.reflection_table.setHorizontalHeaderLabels(["入射角", "吸收率", "吸收能量", "剩余出射能量"])
    
        # Column width settings
        header = self.reflection_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.reflection_table.setColumnWidth(0,30)  # 标号列固定宽度

        # disable editing
        self.reflection_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # center align
        self.reflection_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        # total absorptivity widget
        self.total_absorptivity_widget = TotalAbsorptivityWidget(self)

        result_layout.addWidget(self.reflection_table)
        result_layout.addWidget(self.total_absorptivity_widget)

        # add two widget to left_main_layout
        left_main_layout.addWidget(params_widget, 1)
        left_main_layout.addWidget(laser_reflection_widget, 1)
        left_main_layout.addWidget(result_widget, 10)

        # ------
        button_widget = QWidget()
        button_layout = QVBoxLayout(button_widget)
        button_layout.setContentsMargins(0, 0, 0, 0)
        
        # 激光控制按钮
        self.fire_button = QPushButton("开始")
        self.fire_button.setFixedWidth(80)

        #清空显示台
        self.clear_display_button = QPushButton("清空显示台")
        self.clear_display_button.setFixedWidth(80)

        self.fire_button.clicked.connect(self._on_fire_button_clicked)
        self.clear_display_button.clicked.connect(self._on_clear_display_button_clicked)

        button_layout.addWidget(self.fire_button)
        button_layout.addWidget(self.clear_display_button)
        button_layout.addStretch() 
        
        main_layout.addWidget(left_main_widget, 7) 
        main_layout.addWidget(button_widget, 1) 

    def _on_fire_button_clicked(self):
            self.laser_fire_started.emit()

    def _on_clear_display_button_clicked(self):
        self.clear_display.emit()
    
    # update table data 
    def add_reflection_data(self, data):
        import math
        from PyQt6.QtWidgets import QTableWidgetItem
        from PyQt6.QtCore import Qt
        
        angle_rad = data['angle']
        absorptivity = data['absorptivity']
        remaining_energy = data['remaining_energy']
        absorbed_energy = data['absorbed_energy']
        
        # Convert to display format
        angle_degrees = math.degrees(angle_rad)
        absorptivity_percent = absorptivity * 100
        
        # Add new row
        row_count = self.reflection_table.rowCount()
        self.reflection_table.insertRow(row_count)
        
        # Column 0: Incident angle
        angle_item = QTableWidgetItem(f"{angle_degrees:.1f}°")
        angle_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.reflection_table.setItem(row_count, 0, angle_item)
        
        # Column 1: Absorptivity
        absorption_item = QTableWidgetItem(f"{absorptivity_percent:.2f}%")
        absorption_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.reflection_table.setItem(row_count, 1, absorption_item)
        
        # Column 2: absorbed_energy
        energy_item = QTableWidgetItem(f"{absorbed_energy:.2f}%")
        energy_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.reflection_table.setItem(row_count, 2, energy_item)

        # remaining_energy
        energy_item = QTableWidgetItem(f"{remaining_energy:.2f}%")
        energy_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.reflection_table.setItem(row_count, 3, energy_item)

    def update_total_absorptivity(self, scene_model):
        self.total_absorptivity_widget.update_data(scene_model)
    
    def clear_table(self):
        self.reflection_table.setRowCount(0)
        self.reflection_table.scrollToTop()

        self.total_absorptivity_widget.reset()

    def _update_laser_pos_max(self, hole_radius_value):
        max_value = 2 * hole_radius_value

        self.laser_pos.setMaximum(max_value)
