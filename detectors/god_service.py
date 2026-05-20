from detectors.base import BaseDetector
from parsers.openapi import parse_openapi, find_openapi_files
from parsers.java_parser import find_java_services
import os

class GodServiceDetector(BaseDetector):

    WARNING_THRESHOLD  = 10
    CRITICAL_THRESHOLD = 15

    def get_name(self):
        return "God Service"

    def detect(self, project_path):
        violations = []
        analyzed_services = set()

        # ─── Source 1 : OpenAPI ─────────────────────────
        openapi_files = find_openapi_files(project_path)

        if openapi_files:
            print("   📄 Source : OpenAPI specs")
            for service_name, filepath in openapi_files.items():
                spec  = parse_openapi(filepath)
                nb    = spec["nb_endpoints"]
                title = spec["title"]

                analyzed_services.add(service_name)

                if nb > self.CRITICAL_THRESHOLD:
                    violations.append({
                        "type":         "God Service",
                        "severity":     "CRITICAL",
                        "services":     [service_name],
                        "nb_endpoints": nb,
                        "source":       "OpenAPI",
                        "message":      f"{title} a {nb} endpoints via OpenAPI (seuil: {self.CRITICAL_THRESHOLD})"
                    })
                elif nb > self.WARNING_THRESHOLD:
                    violations.append({
                        "type":         "God Service",
                        "severity":     "WARNING",
                        "services":     [service_name],
                        "nb_endpoints": nb,
                        "source":       "OpenAPI",
                        "message":      f"{title} a {nb} endpoints via OpenAPI (seuil: {self.WARNING_THRESHOLD})"
                    })

        # ─── Source 2 : Annotations Java ────────────────
        # Tourne TOUJOURS — complète OpenAPI
        java_services = find_java_services(project_path)
        java_services = find_java_services(project_path)
        
        if java_services:
            print("   ☕ Source : Java Annotations")
            for service_name, result in java_services.items():

                # Ignorer si déjà analysé via OpenAPI
                if service_name in analyzed_services:
                    continue

                nb = result["total"]

                if nb > self.CRITICAL_THRESHOLD:
                    violations.append({
                        "type":         "God Service",
                        "severity":     "CRITICAL",
                        "services":     [service_name],
                        "nb_endpoints": nb,
                        "source":       "Java Annotations",
                        "message":      f"{service_name} a {nb} endpoints via annotations Java (seuil: {self.CRITICAL_THRESHOLD})"
                    })
                elif nb > self.WARNING_THRESHOLD:
                    violations.append({
                        "type":         "God Service",
                        "severity":     "WARNING",
                        "services":     [service_name],
                        "nb_endpoints": nb,
                        "source":       "Java Annotations",
                        "message":      f"{service_name} a {nb} endpoints via annotations Java (seuil: {self.WARNING_THRESHOLD})"
                    })

        # ─── Aucune source trouvée ───────────────────────
        if not openapi_files and not java_services:
            print("   ⚠️  Aucune source OpenAPI ou Java trouvée")

        return violations