import math
from scipy.optimize import fsolve
import numpy as np

class CollisionDetector:
    
    @staticmethod
    def collision_detector(scene_model):

        laser_func = scene_model.current_segment['path_function'] 
        laser_func_k = laser_func['k']
        laser_func_b = laser_func['b']
        toward_right = scene_model.current_segment['toward_right']

        #当前点的坐标
        current_point_x = scene_model.laser_path[-1][0]
        current_point_y = scene_model.laser_path[-1][1]

        logical_width = scene_model.canvas_width
        logical_height = scene_model.canvas_height

        center_x = logical_width * 0.6
        center_y = logical_height * 0.5

        beam_radius = scene_model.laser_radius
        depth_ratio = scene_model.depth_ratio

        sigma = 20
        A = depth_ratio * beam_radius
        mu = 0

        def equation(t):
            gaussian_x = center_x + A * math.exp(-((t - mu) ** 2) / (2 * sigma ** 2))
            gaussian_y = center_y + t
            laser_y = laser_func_k * gaussian_x + laser_func_b

            return gaussian_y - laser_y 

        t_start = -1.5 * sigma
        t_end = 1.5 * sigma

        initial_guess = np.linspace(t_start, t_end, 30)

        all_intersections = []

        for t_guess in initial_guess:
            try:
                # 优化 fsolve 参数，增加迭代次数并放宽容差
                t_solution = fsolve(equation, t_guess, xtol=1e-6, maxfev=400)[0]
            except:
                # 如果 fsolve 求解失败，忽略这个猜测值并继续
                continue

            #结果有效性
            if t_start <= t_solution <= t_end and abs(equation(t_solution)) <= 1e-6: 
                x = center_x + A * math.exp(-(t_solution - mu) ** 2 / (2 * sigma ** 2)) 
                y = center_y + t_solution

                # 核心修复：检查找到的交点是否与当前点距离过近，防止无限递归
                current_point_x, current_point_y = scene_model.laser_path[-1]
                dist_sq = (x - current_point_x)**2 + (y - current_point_y)**2
                if dist_sq < 1e-6:  # 距离的平方小于一个极小值，认为是同一点
                    continue # 忽略这个解，继续寻找下一个

                if toward_right and x > current_point_x:
                    all_intersections.append((x, y))
                elif not toward_right and x < current_point_x:
                    all_intersections.append((x, y))

        if all_intersections:
            if toward_right:
                closest = min(all_intersections, key=lambda p: p[0])
            else:
                closest = max(all_intersections, key=lambda p: p[0])

            return {
                'collision': True,
                'point': closest
            }
        else:
            
            return {
                'collision': False
            }
