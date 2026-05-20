from detectors.base import BaseDetector
from parsers.properties_parser import find_db_configs
import os

class SharedDbDetector(BaseDetector):

    def get_name(self):
        return "Shared Database"

    def detect(self, services):
        violations = []

        # ─── Source 1 : docker-compose ──────────────────
        db_map = {}

        for service_name, config in services.items():
            db_host   = config.get("db_host")
            db_schema = config.get("db_schema")

            if db_host is None or db_schema is None:
                continue

            # Ignorer les variables non résolues
            if db_host.startswith('$') or \
               db_schema.startswith('$'):
                # Grouper quand même par variable
                db_key = f"{db_host}/{db_schema}"
            else:
                db_key = f"{db_host}/{db_schema}"

            if db_key not in db_map:
                db_map[db_key] = {
                    "services": [],
                    "source":   "docker-compose"
                }
            db_map[db_key]["services"].append(service_name)

        for db_key, info in db_map.items():
            if len(info["services"]) > 1:
                violations.append({
                    "type":     "Shared Database",
                    "severity": "CRITICAL",
                    "services": info["services"],
                    "source":   info["source"],
                    "database": db_key,
                    "message":  f"{len(info['services'])} services partagent la même base : {db_key}"
                })

        return violations

    def detect_from_configs(self, project_path):
        """
        Source 2, 3, 5 :
        Détection via .properties, application.yml, .env
        """
        violations = []

        # Chercher tous les fichiers de config
        db_configs = find_db_configs(project_path)

        if not db_configs:
            return []

        # Grouper par DB
        db_map = {}

        for service_name, db_info in db_configs.items():
            db_host   = db_info.get('db_host')
            db_schema = db_info.get('db_schema')

            if not db_host or not db_schema:
                continue

            db_key = f"{db_host}/{db_schema}"

            if db_key not in db_map:
                db_map[db_key] = {
                    "services": [],
                    "source":   "config files"
                }
            db_map[db_key]["services"].append(service_name)

        for db_key, info in db_map.items():
            if len(info["services"]) > 1:
                violations.append({
                    "type":     "Shared Database",
                    "severity": "CRITICAL",
                    "services": info["services"],
                    "source":   info["source"],
                    "database": db_key,
                    "message":  f"{len(info['services'])} services partagent la même base via config files : {db_key}"
                })

        return violations