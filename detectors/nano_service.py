from detectors.base import BaseDetector
from parsers.openapi import find_openapi_files, parse_openapi
from parsers.java_parser import find_java_services


class NanoServiceDetector(BaseDetector):
    """
    Détecte les microservices trop petits (< 3 endpoints).
    
    Un Nano Service a trop peu de responsabilités pour justifier
    les coûts opérationnels d'un microservice autonome (DB, CI/CD, monitoring).
    """
    
    THRESHOLD = 3  # Seuil configurable
    
    def get_name(self):
        return "Nano Service"
    
    def detect(self, project_path):
        violations = []
        endpoint_counts = {}
        
        # Source 1: OpenAPI / Swagger
        openapi_files = find_openapi_files(project_path)
        for service, openapi_path in openapi_files.items():
            try:
                data = parse_openapi(openapi_path)
                endpoint_counts[service] = data["nb_endpoints"]
            except Exception:
                continue
        
        # Source 2: Annotations Java (fallback si pas d'OpenAPI)
        java_services = find_java_services(project_path)
        for service, data in java_services.items():
            if service not in endpoint_counts:  # Éviter les doublons
                endpoint_counts[service] = data["total"]
        
        # Détection des Nano Services
        for service, count in endpoint_counts.items():
            if 0 < count < self.THRESHOLD:
                violations.append({
                    "type": "Nano Service",
                    "severity": "WARNING",
                    "services": [service],
                    "message": f"{service} a seulement {count} endpoint(s) — trop petit pour justifier un microservice autonome"
                })
        
        return violations
