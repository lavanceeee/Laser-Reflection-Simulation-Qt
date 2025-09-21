import math

class SceneModel:
    def __init__(self):

        self.laser_radius = 25

        self.depth_ratio = 2

        self.A = self.laser_radius * self.depth_ratio

        self.laser_position = 25

        self.sigma = 20

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

        return  self.A * math.exp(-((t - 0) ** 2) / (2 * self.sigma ** 2))

    #求导函数
    def gaussian_derivative(self, t):

        return -self.A * t / (self.sigma ** 2) * math.exp(-((t - 0) ** 2) / (2 * self.sigma ** 2))
