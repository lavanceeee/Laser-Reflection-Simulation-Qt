import math
"""
更新激光的函数

当前坐标 
曲线在这里的切线
当前函数和法线确定接下来的新的激光函数
"""
class UpdateLaser:

    @staticmethod
    def update_laser(scene_model):
        #最新的位置信息
        current_pos_x, current_pos_y = scene_model.laser_path[-1]

        #入射光线的斜率
        incident_slope = scene_model.current_segment['path_function']['k']

        # fix: 补偿mu偏移量
        center_y = scene_model.canvas_height * 0.5 - scene_model.mu
        t = current_pos_y - center_y

        #该点处的斜率
        dx_dy = scene_model.gaussian_derivative(t)  # 这是dx/dy
        
        # 这里有问题：转换为切线斜率dy/dx
        if abs(dx_dy) < 1e-10:
            k = float('inf')  # 垂直切线
        else:
            k = 1 / dx_dy  # dy/dx = 1/(dx/dy)
        
        # 切线斜率
        scene_model.tangent_slopes.append(k)

        #法线斜率为零的情况
        if abs(k) < 1e-10:
            normal_slope = float('inf')
        else:
            #法线的斜率
            normal_slope = -1/k
            
        reflection_slope = UpdateLaser._calculate_reflection_slope(scene_model, incident_slope, normal_slope)

        scene_model.current_segment['path_function']['k'] = reflection_slope

        b = current_pos_y - reflection_slope * current_pos_x

        scene_model.current_segment['path_function']['b'] = b

        # #法线朝左的方向向量
        # n_vector = (-1, -normal_slope)
        # #激光朝右的方向向量
        # v_vector = (1, reflection_slope)

        #点积判断两者的夹角大小
        dot_product = -1 + -normal_slope * reflection_slope
        
        if dot_product > 0:
            #朝右
            scene_model.current_segment['toward_right'] = True
        else:
            scene_model.current_segment['toward_right'] = False

        #更新segment_id
        scene_model.current_segment['segment_id'] += 1

    @staticmethod
    def _calculate_reflection_slope(scene_model, incident_slope, normal_slope):
        #角度转为弧度
        incident_angle = math.atan(incident_slope)
        normal_angle = math.atan(normal_slope)

        #相对于法线入射角大小
        relative_incident_angle = incident_angle - normal_angle

        # record absolute value of incident angle into array
        scene_model.incident_angle.append(abs(relative_incident_angle))

        #反射角 = -入射角
        relative_reflection_angle = -relative_incident_angle

        #反射光线的绝对角度
        reflection_angle = normal_angle + relative_reflection_angle

        #转回斜率
        return math.tan(reflection_angle)