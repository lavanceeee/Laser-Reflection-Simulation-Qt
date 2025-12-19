import math

class AbsorptivityRate:
    def __init__(self):
        
        # 复反射率
        self.refractive_index = 4.2231 # 实部 折射率
        
        self.extinction_coefficient = 0.061005 # 虚部 消光系数

    def absorptivity_rate_calcuate(self, incident_angle_rad):
        n_magnitude = math.sqrt(
            self.refractive_index ** 2 +
            self.extinction_coefficient ** 2
        )

        # 避免用户将折射率调整为 0 导致除零或非法反三角函数运算
        n_magnitude = max(n_magnitude, 1e-8)

        sin_reflective = math.sin(incident_angle_rad) / n_magnitude
        sin_reflective = max(min(sin_reflective, 1.0), -1.0)
        reflective_angle_rad = math.asin(sin_reflective)

        Rs = (
            (math.cos(incident_angle_rad) - self.refractive_index * math.cos(reflective_angle_rad)) / 
            (math.cos(incident_angle_rad) + self.refractive_index * math.cos(reflective_angle_rad))
            ) ** 2

        Rp = (
            (math.cos(reflective_angle_rad) - self.refractive_index * math.cos(incident_angle_rad)) / 
            (math.cos(reflective_angle_rad) + self.refractive_index * math.cos(incident_angle_rad))
            ) ** 2

        R = (Rs + Rp) / 2

        A = 1 - R

        return A, R
