import math
import numpy as np
from app.core.scene_model import SceneModel

class GaussianEquation:
    @staticmethod
    def calculate_gaussian_points(center_x, center_y, scene_model):
        points = []

        mu = scene_model.mu
        hole_radius = scene_model.hole_radius

        x_start = mu - hole_radius
        x_end =  mu + hole_radius

        # laser beams
        x_values = np.linspace(x_start, x_end, 10000)

        gaussian_values = scene_model.gaussian_equation(x_values)
        screen_x_values = center_x + gaussian_values
        screen_y_values = center_y + x_values

        points = list(zip(screen_x_values, screen_y_values))

        return points