import numpy as np

class SceneModel:
    def __init__(self):

        self.laser_radius = 25

        self.depth_ratio = 2

        self.laser_position = 25

        self.sigma = 20

        self.mu = 25

        self.hole_radius = 25

        self.mms = self.hole_radius * self.depth_ratio * self.sigma * np.sqrt(2 * np.pi) / (1 - np.exp(-self.mu**2 / (2 * self.sigma**2)))
        
        self.A = self.mms / (self.sigma * np.sqrt(2 * np.pi))

        #激光点坐标
        self.laser_pos = (0, 0)
        self.is_firing = False
        self.laser_path = []

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

        #画布宽高
        self.canvas_width = 0
        self.canvas_height = 0
        
        # 切线斜率
        self.tangent_slopes = []

    def gaussian_equation(self, t):
        return  self.A * np.exp(-((t - self.mu) ** 2) / (2 * self.sigma ** 2))

    #求导函数
    def gaussian_derivative(self, t):
        return -self.A * (t - self.mu) / (self.sigma ** 2) * np.exp(-((t - self.mu) ** 2) / (2 * self.sigma ** 2))

    def reset_model(self):
        self.laser_path = []

        self.tangent_slopes = []

        self.is_firing = False

        #坑：忘记更新直线为水平了
        self.current_segment = {
            'toward_right': True,
            'step_size': 3,
            'path_function': {
                'k': 0,          
                'b': self.laser_pos[1]
            },
            'segment_id': 0
        }


