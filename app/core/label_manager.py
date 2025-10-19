import math

class LabelData:
    def __init__(self, anchor_point, reflection_data):
        self.anchor_point = anchor_point
        self.angle = reflection_data['angle']
        self.absorptivity = reflection_data['absorptivity']
        self.index = reflection_data['index']

        directions = [
            (0, -1),   
            (0, 5) 
        ]

        # label position
        offset_x, offset_y = directions[self.index % len(directions)]
        print(offset_x, offset_y)
        self.display_position = (anchor_point[0] + offset_x, anchor_point[1] + offset_y)

        self.text_lines = [   
            f"第{self.index + 1}次反射",       
            f"入射角：{math.degrees(self.angle):.2f}°",  
            f"吸收率: {self.absorptivity * 100:.2f}%",
            f"反射率：{100.0 - self.absorptivity * 100:.2f}%"
        ]

class LabelManager:
    def __init__(self):
        self.labels = []

    def add_label(self, anchor_point, reflection_data):
        label = LabelData(anchor_point, reflection_data)
        self.labels.append(label)
    
    def clear_labels(self):
        self.labels = []

        