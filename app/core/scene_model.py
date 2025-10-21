import numpy as np

class SceneModel:
    def __init__(self):
        # 画布宽高
        self.canvas_width = 0
        self.canvas_height = 0

        self.laser_radius = 25
        self.depth_ratio = 2.0
        self.laser_position = 25

        self.sigma = 20
        self.mu = 25
        
        self.hole_radius = 25
        self._update_hole_paramters()

        # laser position
        self.laser_pos = (0, 0)

        self.is_firing = False
        self.laser_path = []
        self.incident_angle = []
        self.current_energy = 100.0

        self.reflection_data = [] 
        self.incident_angle = []

        #每一段光线路径
        self.current_segment = {
            'toward_right': True,
            'step_size': 3,
            'path_function': {
                'k': 0, 
                'b': 0
            },
            'segment_id': 0
        }

        # 切线斜率
        self.tangent_slopes = []

    # 孔洞高斯函数
    def gaussian_equation(self, t):
        return  self.A * np.exp(-((t - self.mu) ** 2) / (2 * self.sigma ** 2))

    # 导函数
    def gaussian_derivative(self, t):
        return -self.A * (t - self.mu) / (self.sigma ** 2) * np.exp(-((t - self.mu) ** 2) / (2 * self.sigma ** 2))

    def reset_model(self):
        self.laser_path = []

        self.tangent_slopes = []

        self.is_firing = False

        # fix：更新直线为水平
        self.current_segment = {
            'toward_right': True,
            'step_size': 3,
            'path_function': {
                'k': 0,          
                'b': self.laser_pos[1]
            },
            'segment_id': 0
        }

        # clear table data
        self.reflection_data = []
        self.incident_angle = []
        self.current_energy = 100.0

    def _update_hole_paramters(self):
        self.mms = (
            self.hole_radius * 
            self.depth_ratio * 
            self.sigma * 
            np.sqrt(2 * np.pi) / 
            (1 - np.exp(-self.mu**2 / (2 * self.sigma**2)))
        )

        self.A = (
            self.mms / 
            (self.sigma * np.sqrt(2 * np.pi))
        )

    def set_hole_radius(self, hole_radius):
        self.hole_radius = hole_radius
        self._update_hole_paramters()

    def set_depth_ratio(self, depth_ratio):
        self.depth_ratio = depth_ratio
        self._update_hole_paramters()

