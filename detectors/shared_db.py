from detectors.base import BaseDetector

class SharedDbDetector(BaseDetector):
    
    def get_name(self):
        return "Shared Database"
    
    def detect(self, services):
        """
        Détecte si plusieurs services partagent
        la même base de données.
        """
        
        # Regrouper les services par DB_HOST + DB_SCHEMA
        db_map = {}
        
        for service_name, config in services.items():
            db_host   = config.get("db_host")
            db_schema = config.get("db_schema")
            
            # Ignorer les services sans base de données
            if db_host is None or db_schema is None:
                continue
            
            # Clé unique = host + schema
            db_key = f"{db_host}/{db_schema}"
            
            if db_key not in db_map:
                db_map[db_key] = []
            
            db_map[db_key].append(service_name)
        
        # Détecter les violations
        violations = []
        
        for db_key, service_list in db_map.items():
            if len(service_list) > 1:
                violations.append({
                    "type":      "Shared Database",
                    "severity":  "CRITICAL",
                    "database":  db_key,
                    "services":  service_list,
                    "message":   f"{len(service_list)} services partagent la même base : {db_key}"
                })
        
        return violations