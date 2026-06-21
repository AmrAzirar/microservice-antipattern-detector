import yaml
import os
import re

def parse_properties_file(filepath):
    """
    Parse un fichier application.properties
    et extrait les connexions DB
    """
    db_info = {}

    try:
        with open(filepath, 'r',
                 encoding='utf-8',
                 errors='ignore') as f:
            for line in f:
                line = line.strip()

                # Ignorer commentaires et lignes vides
                if line.startswith('#') or '=' not in line:
                    continue

                key, value = line.split('=', 1)
                key   = key.strip().lower()
                value = value.strip()

                # Chercher les URLs de DB
                if any(k in key for k in [
                    'datasource.url',
                    'db.url',
                    'database.url',
                    'jdbc.url'
                ]):
                    db_info['db_url'] = value
                    # Extraire host et db depuis jdbc URL
                    # jdbc:mysql://HOST:PORT/DB_NAME
                    match = re.search(
                        r'jdbc:\w+://([^:/]+)(?::\d+)?/(\w+)',
                        value
                    )
                    if match:
                        db_info['db_host']   = match.group(1)
                        db_info['db_schema'] = match.group(2)

    except Exception as e:
        print(f"⚠️  Erreur parsing {filepath}: {e}")

    return db_info


def parse_application_yml(filepath):
    """
    Parse un fichier application.yml Spring Boot
    et extrait les connexions DB
    """
    db_info = {}

    try:
        with open(filepath, 'r',
                 encoding='utf-8',
                 errors='ignore') as f:
            config = yaml.safe_load(f)

        if not config:
            return db_info

        # spring.datasource.url
        spring = config.get('spring', {})
        if spring:
            datasource = spring.get('datasource', {})
            if datasource:
                url = datasource.get('url', '')
                if url:
                    db_info['db_url'] = url
                    match = re.search(
                        r'jdbc:\w+://([^:/]+)(?::\d+)?/(\w+)',
                        url
                    )
                    if match:
                        db_info['db_host']   = match.group(1)
                        db_info['db_schema'] = match.group(2)

    except Exception as e:
        print(f"⚠️  Erreur parsing {filepath}: {e}")

    return db_info


def parse_env_file(filepath):
    """
    Parse un fichier .env
    et extrait les connexions DB
    """
    db_info = {}

    try:
        with open(filepath, 'r',
                 encoding='utf-8',
                 errors='ignore') as f:
            for line in f:
                line = line.strip()

                if line.startswith('#') or '=' not in line:
                    continue

                key, value = line.split('=', 1)
                key   = key.strip().upper()
                value = value.strip()

                # Ignorer les variables d'environnement
                if value.startswith('$'):
                    continue

                if key in ['DB_HOST', 'DATABASE_HOST',
                           'MYSQL_HOST', 'POSTGRES_HOST']:
                    db_info['db_host'] = value

                if key in ['DB_NAME', 'DB_SCHEMA',
                           'DATABASE_NAME', 'MYSQL_DATABASE',
                           'POSTGRES_DB']:
                    db_info['db_schema'] = value

    except Exception as e:
        print(f"⚠️  Erreur parsing {filepath}: {e}")

    return db_info


def find_db_configs(project_path):
    """
    Cherche tous les fichiers de config DB
    dans les sous-dossiers du projet.
    Retourne un dict : service_name → db_info
    """
    from parsers.java_parser import is_microservice
    results = {}

    for root, dirs, files in os.walk(project_path):

        # Ignorer dossiers non pertinents
        dirs[:] = [d for d in dirs
                  if d not in ['.git', 'target',
                               'node_modules', 'venv',
                               '__pycache__']]

        for filename in files:
            filepath = os.path.join(root, filename)
            db_info  = {}

            # Source 2 — .properties
            if filename == 'application.properties':
                db_info = parse_properties_file(filepath)

            # Source 3 — application.yml
            elif filename == 'application.yml':
                db_info = parse_application_yml(filepath)

            # Source 5 — .env
            elif filename == '.env':
                db_info = parse_env_file(filepath)

            if db_info.get('db_host') and \
               db_info.get('db_schema'):

                # Trouver le vrai service parent
                service_name = None
                path = os.path.dirname(filepath)

                while path != project_path and \
                      path != os.path.dirname(path):
                    if is_microservice(path):
                        service_name = os.path.basename(path)
                        break
                    path = os.path.dirname(path)

                # Fallback si pas trouvé
                if not service_name:
                    parts = filepath.replace('\\', '/').split('/')
                    project_parts = project_path.replace(
                        '\\', '/').split('/')
                    idx = len(project_parts)
                    if idx < len(parts):
                        service_name = parts[idx]
                    else:
                        service_name = os.path.basename(root)

                # Éviter les doublons
                if service_name not in results:
                    results[service_name] = db_info

    return results