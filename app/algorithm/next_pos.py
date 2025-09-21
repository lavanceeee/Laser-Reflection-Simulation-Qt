from unittest import result
from app.algorithm.collision_detector import CollisionDetector

class NextPosition:
    
    @staticmethod
    def calcuate_next_pos(current_position, scene_model):

        result = CollisionDetector.collision_detector(scene_model)

        if result['collision']:
            return result['point']
        else:
            return None




