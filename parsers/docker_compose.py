import yaml
import os

def parse_docker_compose(filepath):
    """
    Parse un fichier docker-compose.yml et extrait
    les informations de chaque service.
    """
    
    # Vérifier que le fichier existe
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Fichier non trouvé : {filepath}")
    
    # Lire et parser le fichier YAML
    with open(filepath, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    services = config.get("services", {})
    result = {}

    for service_name, service_config in services.items():
        
        # Extraire les variables d'environnement
        env = service_config.get("environment", {})
        
        # Convertir liste en dict si nécessaire
        # ["DB_HOST=mysql"] → {"DB_HOST": "mysql"}
        if isinstance(env, list):
            env_dict = {}
            for item in env:
                if "=" in item:
                    key, value = item.split("=", 1)
                    env_dict[key] = value
            env = env_dict
        
        # Extraire depends_on
        depends_on = service_config.get("depends_on", {})
        if isinstance(depends_on, list):
            deps = depends_on
        else:
            deps = list(depends_on.keys())
        
        # Stocker les infos du service
        result[service_name] = {
            "db_host":   env.get("DB_HOST"),
            "db_schema": env.get("DB_SCHEMA"),
            "db_port":   env.get("DB_PORT"),
            "depends_on": deps
        }
    
    return result