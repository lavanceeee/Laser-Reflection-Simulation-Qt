from PyQt6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget, QSpinBox, QPushButton
from PyQt6.QtCore import pyqtSignal

class ControlPanel(QWidget):

    beam_radius_changed = pyqtSignal(int)
    depth_ratio_changed = pyqtSignal(int)
    laser_position_changed = pyqtSignal(int)
    laser_fire_started = pyqtSignal()
    clear_display = pyqtSignal()


    def __init__(self):
        super().__init__()
        self.setStyleSheet("border: 1px solid red;")
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QHBoxLayout(self)
        
        # 左侧
        params_widget = QWidget()
        params_layout = QVBoxLayout(params_widget)
        
        #激光半径
        beam_layout = QHBoxLayout()
        beam_layout.addWidget(QLabel("激光半径："))
        self.beam_radius = QSpinBox()
        self.beam_radius.setValue(25)
        self.beam_radius.valueChanged.connect(self.beam_radius_changed.emit)
        beam_layout.addWidget(self.beam_radius)
        beam_layout.addStretch() 
        params_layout.addLayout(beam_layout)

        #深径比
        depth_layout = QHBoxLayout()
        depth_layout.addWidget(QLabel("深径比："))
        self.depth_ratio = QSpinBox()
        self.depth_ratio.setValue(2)
        self.depth_ratio.valueChanged.connect(self.depth_ratio_changed.emit)
        depth_layout.addWidget(self.depth_ratio)
        depth_layout.addStretch()
        params_layout.addLayout(depth_layout)

        #激光入射坐标
        position_layout = QHBoxLayout()
        position_layout.addWidget(QLabel("入射坐标："))
        self.laser_pos = QSpinBox()
        self.laser_pos.setValue(25)
        self.laser_pos.valueChanged.connect(self.laser_position_changed.emit)
        position_layout.addWidget(self.laser_pos)
        position_layout.addStretch()
        params_layout.addLayout(position_layout)
        
        # 右侧
        button_widget = QWidget()
        button_layout = QVBoxLayout(button_widget)
        
        # 激光控制按钮
        self.fire_button = QPushButton("开始")
        self.fire_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #FF5722;
            }
        """)

        #清空显示台
        self.clear_display_button = QPushButton("清空显示台")
        self.clear_display_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #FF5722;
            }
        """)

        self.fire_button.clicked.connect(self._on_fire_button_clicked)
        self.clear_display_button.clicked.connect(self._on_clear_display_button_clicked)

        button_layout.addWidget(self.fire_button)
        button_layout.addWidget(self.clear_display_button)
        button_layout.addStretch()  # 按钮顶部对齐
        
        main_layout.addWidget(params_widget, 3)  # 左侧占3份
        main_layout.addWidget(button_widget, 1)  # 右侧占1份

        # # 激光发射状态
        # self.is_firing = False

    def _on_fire_button_clicked(self):
        # if not self.is_firing:
            # 开始发射
            # self.is_firing = True
            # self.fire_button.setStyleSheet("""
            #     QPushButton {
            #         background-color: #FF5722;
            #         color: white;
            #         border: none;
            #         padding: 12px 24px;
            #         border-radius: 6px;
            #         font-weight: bold;
            #         font-size: 14px;
            #         min-width: 80px;
            #     }
            #     QPushButton:hover {
            #         background-color: #E64A19;
            #     }
            # """)
            self.laser_fire_started.emit()

    def _on_clear_display_button_clicked(self):
        self.clear_display.emit()