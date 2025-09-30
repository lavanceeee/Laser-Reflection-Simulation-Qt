from PyQt6.QtWidgets import QHBoxLayout, QLabel, QTableWidget, QHeaderView, QVBoxLayout, QWidget, QSpinBox, QPushButton
from PyQt6.QtCore import pyqtSignal

class ControlPanel(QWidget):

    beam_radius_changed = pyqtSignal(int)
    depth_ratio_changed = pyqtSignal(int)
    laser_position_changed = pyqtSignal(int)
    laser_fire_started = pyqtSignal()
    clear_display = pyqtSignal()
    hole_radius_changed = pyqtSignal(int)


    def __init__(self):
        super().__init__()
        self.setStyleSheet("border: 1px solid red;")
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QHBoxLayout(self)
        
        # paramter selector and result area 
        left_main_widget = QWidget()
        left_main_layout = QHBoxLayout(left_main_widget)

        params_widget = QWidget()
        params_layout = QVBoxLayout(params_widget)
        
        # laser_radius
        beam_layout = QHBoxLayout()
        beam_layout.addWidget(QLabel("激光半径："))
        self.beam_radius = QSpinBox()
        self.beam_radius.setValue(25)
        self.beam_radius.valueChanged.connect(self.beam_radius_changed.emit)
        beam_layout.addWidget(self.beam_radius)
        beam_layout.addStretch() 
        params_layout.addLayout(beam_layout)

        # hole_radius
        hole_radius_layout = QHBoxLayout()
        hole_radius_layout.addWidget(QLabel("孔洞半径："))
        self.hole_radius = QSpinBox()
        self.hole_radius.setValue(25)
        self.hole_radius.valueChanged.connect(self.hole_radius_changed.emit)
        hole_radius_layout.addWidget(self.hole_radius)
        hole_radius_layout.addStretch()
        params_layout.addLayout(hole_radius_layout)

        #depth_ratio
        depth_layout = QHBoxLayout()
        depth_layout.addWidget(QLabel("深径比(孔洞深度h/半径r)："))
        self.depth_ratio = QSpinBox()
        self.depth_ratio.setValue(2)
        self.depth_ratio.valueChanged.connect(self.depth_ratio_changed.emit)
        depth_layout.addWidget(self.depth_ratio)
        depth_layout.addStretch()
        params_layout.addLayout(depth_layout)

        # laser_position
        position_layout = QHBoxLayout()
        position_layout.addWidget(QLabel("入射坐标："))
        self.laser_pos = QSpinBox()
        self.laser_pos.setValue(25)
        self.laser_pos.valueChanged.connect(self.laser_position_changed.emit)
        position_layout.addWidget(self.laser_pos)
        position_layout.addStretch()
        params_layout.addLayout(position_layout)

        # right result panel of left_main_layout
        result_widget = QWidget()
        result_layout = QVBoxLayout(result_widget)

        # create table
        self.reflection_table = QTableWidget()
        self.reflection_table.setColumnCount(4)
        self.reflection_table.setHorizontalHeaderLabels(["index", "Angle", "Absorptivity", "Reflectivity"])
        
        # Table style
        self.reflection_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #ddd;
                gridline-color: #e0e0e0;
                font-size: 12px;
            }
            QTableWidget::item {
                padding: 5px;
                border-bottom: 1px solid #f0f0f0;
            }
            QTableWidget::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 8px;
                border: none;
                border-bottom: 2px solid #ddd;
                font-weight: bold;
                color: #555;
            }
        """)
        
        # Column width settings
        header = self.reflection_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.reflection_table.setColumnWidth(0, 60)  # 标号列固定宽度

        # disable editing
        self.reflection_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # center align
        self.reflection_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        result_layout.addWidget(self.reflection_table)

        # add two widget to left_main_layout
        left_main_layout.addWidget(params_widget, 1)
        left_main_layout.addWidget(result_widget, 3)

        # ------
        
        # 右侧
        button_widget = QWidget()
        button_layout = QVBoxLayout(button_widget)
        
        # 激光控制按钮
        self.fire_button = QPushButton("开始")

        #清空显示台
        self.clear_display_button = QPushButton("清空显示台")

        self.fire_button.clicked.connect(self._on_fire_button_clicked)
        self.clear_display_button.clicked.connect(self._on_clear_display_button_clicked)

        button_layout.addWidget(self.fire_button)
        button_layout.addWidget(self.clear_display_button)
        button_layout.addStretch() 
        
        main_layout.addWidget(left_main_widget, 5) 
        main_layout.addWidget(button_widget, 1) 

    def _on_fire_button_clicked(self):
            self.laser_fire_started.emit()

    def _on_clear_display_button_clicked(self):
        self.clear_display.emit()