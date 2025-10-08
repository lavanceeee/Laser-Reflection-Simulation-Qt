from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt

class TotalAbsorptivityWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self._setup_ui()
        self.reset()

    # def _setup_ui(self):
    #     self.setMinimumHeight(35)

    def reset(self):
        self.setText("Total absorptivity:")

    def update_data(self, scene_model):
        if not scene_model.reflection_data:
            self.reset()
            return

        latest_reflection = scene_model.reflection_data[-1]
        remaining_energy = latest_reflection['remaining_energy']

        total_absorptivity = 100.0 - remaining_energy

        self.setText(f"Total absorptivity: {total_absorptivity:.2f}%")
        


    