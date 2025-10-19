from app.algorithm.absorptivity_rate import AbsorptivityRate

class EnergyTracker:
    def __init__(self):

        self.absorptivity_calculator = AbsorptivityRate()

    # record each 
    def calcuate_and_record(self, scene_model, incident_angle_rad):
        A, R = self.absorptivity_calculator.absorptivity_rate_calcuate(incident_angle_rad)

        # 吸收的能量
        absorbed_energy = scene_model.current_energy * A
        
        # 剩余出射能量
        scene_model.current_energy *= R

        scene_model.reflection_data.append({
            'index': len(scene_model.reflection_data),
            'angle': incident_angle_rad,
            'absorptivity': A,
            'remaining_energy': scene_model.current_energy,
            'absorbed_energy': absorbed_energy
        })