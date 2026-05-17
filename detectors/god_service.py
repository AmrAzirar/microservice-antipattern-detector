from detectors.base import BaseDetector
from parsers.openapi import parse_openapi, find_openapi_files

class GodServiceDetector(BaseDetector):

    # Seuils de détection
    WARNING_THRESHOLD  = 10
    CRITICAL_THRESHOLD = 15

    def get_name(self):
        return "God Service"

    def detect(self, project_path):
        """
        Détecte les God Services en comptant
        les endpoints dans les fichiers OpenAPI.
        """

        violations = []

        # Chercher tous les fichiers openapi.yaml
        openapi_files = find_openapi_files(project_path)

        if not openapi_files:
            return []

        for service_name, filepath in openapi_files.items():
            spec     = parse_openapi(filepath)
            nb       = spec["nb_endpoints"]
            title    = spec["title"]

            if nb > self.CRITICAL_THRESHOLD:
                violations.append({
                    "type":         "God Service",
                    "severity":     "CRITICAL",
                    "services":     [service_name],
                    "nb_endpoints": nb,
                    "message":      f"{title} a {nb} endpoints (seuil: {self.CRITICAL_THRESHOLD})"
                })

            elif nb > self.WARNING_THRESHOLD:
                violations.append({
                    "type":         "God Service",
                    "severity":     "WARNING",
                    "services":     [service_name],
                    "nb_endpoints": nb,
                    "message":      f"{title} a {nb} endpoints (seuil: {self.WARNING_THRESHOLD})"
                })

        return violations