def reset_before_update(func):
    def wrapper(self, *args, **kwargs):
        if hasattr(self, 'scene_model') and self.scene_model.is_firing:
            self.scene_model.reset_model()
            
            if hasattr(self, 'clear_table_signal'):
                self.clear_table_signal.emit()
            
            if hasattr(self, 'label_manager'):
                self.label_manager.clear_labels()
            
            if hasattr(self, 'update'):
                self.update()

        # 执行原来的方法
        return func(self, *args, **kwargs)
    
    return wrapper
