class BaseDetector:
    """Classe de base pour tous les détecteurs"""
    
    def detect(self, data):
        raise NotImplementedError
    
    def get_name(self):
        raise NotImplementedError