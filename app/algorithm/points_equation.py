import math

class GaussianEquation:

    @staticmethod
    def calculate_gaussian_points(center_x, center_y, beam_radius, depth_ratio):
        
        points = []

        sigma = 20
        A = depth_ratio * beam_radius
        mu = 0

        x_start = - 1.5 * sigma
        x_end =  1.5 * sigma
        step = 0.5

        x = x_start
        while x <= x_end:
            
            exponent = -((x - mu) ** 2) / (2 * sigma ** 2)
            gaussian_value = A * math.exp(exponent)

            screen_x = center_x + gaussian_value
            screen_y = center_y + x

            points.append((screen_x, screen_y))

            x += step

        return points
