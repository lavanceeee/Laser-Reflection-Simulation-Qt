import math

class LabelData:
    def __init__(self, anchor_point, reflection_data):
        self.anchor_point = anchor_point
        self.angle = reflection_data['angle']
        self.absorptivity = reflection_data['absorptivity']
        self.remaining_energy = reflection_data['remaining_energy']

        # label position
        self.display_position = (anchor_point[0] + 10, anchor_point[1]-10)

        self.text_lines = [          
            f"入射角：{math.degrees(self.angle):.2f}°",  
            f"吸收率: {self.absorptivity*100:.2f}%",
            f"剩余能量: {self.remaining_energy:.2f}%"
        ]

class LabelManager:
    def __init__(self):
        self.labels = []

    def add_label(self, anchor_point, reflection_data):
        label = LabelData(anchor_point, reflection_data)
        self.labels.append(label)

        return label
    
    def clear_labels(self):
        self.labels = []

        