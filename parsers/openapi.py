import yaml
import os

def parse_openapi(filepath):
    """
    Parse un fichier openapi.yaml et extrait
    le nombre d'endpoints par service.
    """

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Fichier non trouvé : {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        spec = yaml.safe_load(f)

    # Extraire le nom du service
    info     = spec.get("info", {})
    title    = info.get("title", "Unknown Service")

    # Compter les endpoints
    paths    = spec.get("paths", {})
    
    http_methods = ["get", "post", "put", 
                    "delete", "patch", "options"]
    
    endpoints = []
    
    for path, methods in paths.items():
        for method in http_methods:
            if method in methods:
                endpoints.append({
                    "path":   path,
                    "method": method.upper()
                })

    return {
        "title":         title,
        "nb_endpoints":  len(endpoints),
        "endpoints":     endpoints
    }


def find_openapi_files(project_path):
    """
    Cherche tous les fichiers openapi.yaml
    dans les sous-dossiers du projet.
    """
    openapi_files = {}

    for root, dirs, files in os.walk(project_path):
        for filename in files:
            if filename in ["openapi.yaml", 
                           "openapi.yml",
                           "swagger.yaml",
                           "swagger.yml"]:
                filepath = os.path.join(root, filename)
                # Nom du service = nom du dossier parent
                service_name = os.path.basename(root)
                openapi_files[service_name] = filepath

    return openapi_files