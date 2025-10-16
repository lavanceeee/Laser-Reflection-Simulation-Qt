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

        sin_reflective = math.sin(incident_angle_rad) / n_magnitude
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