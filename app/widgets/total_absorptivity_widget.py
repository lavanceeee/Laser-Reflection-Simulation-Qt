from PyQt6.QtWidgets import QLabel

class TotalAbsorptivityWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QLabel {
                color: #dc3545;
                font-size: 16px;
                font-weight: 600;
            }
        """)
        self.reset()

    def reset(self):
        self.setText("总吸收率:")

    def update_data(self, scene_model):
        if not scene_model.reflection_data:
            self.reset()
            return

        latest_reflection = scene_model.reflection_data[-1]
        remaining_energy = latest_reflection['remaining_energy']

        total_absorptivity = 100.0 - remaining_energy

        self.setText(f"总吸收率: {total_absorptivity:.2f}%")