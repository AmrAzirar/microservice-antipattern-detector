import os
import re


def is_controller_file(content):
    """
    Vérifie si le fichier Java est un Controller
    """
    return any(annotation in content for annotation in [
        '@RestController',
        '@Controller'
    ])


def is_microservice(service_path):
    """
    Vérifie si un dossier est un vrai microservice
    en cherchant des fichiers indicateurs
    """
    indicators = [
        'pom.xml',
        'build.gradle',
        'package.json',
        'requirements.txt',
        'Dockerfile',
        'application.properties',
        'application.yml'
    ]
    try:
        files = os.listdir(service_path)
        return any(ind in files for ind in indicators)
    except Exception:
        return False


def count_endpoints_from_java(service_path):
    """
    Compte les endpoints depuis les annotations
    Spring Boot dans les fichiers Java
    """
    endpoint_annotations = [
        r'@GetMapping',
        r'@PostMapping',
        r'@PutMapping',
        r'@DeleteMapping',
        r'@PatchMapping',
        r'@RequestMapping\s*\(',
    ]

    total_endpoints = 0
    files_analyzed  = []

    for root, dirs, files in os.walk(service_path):

        dirs[:] = [d for d in dirs
                  if d not in [
                      '.git', 'target',
                      'node_modules', 'venv',
                      '__pycache__', 'test',
                      'tests'
                  ]]

        for filename in files:
            if not filename.endswith('.java'):
                continue

            filepath = os.path.join(root, filename)

            try:
                with open(filepath, 'r',
                         encoding='utf-8',
                         errors='ignore') as f:
                    content = f.read()

                if not is_controller_file(content):
                    continue

                file_count = 0
                for pattern in endpoint_annotations:
                    matches = re.findall(pattern, content)
                    file_count += len(matches)

                if file_count > 0:
                    total_endpoints += file_count
                    files_analyzed.append({
                        "file":      filename,
                        "endpoints": file_count
                    })

            except Exception:
                continue

    return {
        "total":  total_endpoints,
        "files":  files_analyzed,
        "source": "Java Annotations"
    }


def find_java_services(project_path):
    """
    Trouve tous les vrais microservices Java
    Gère toutes les structures de projets :
    - project/service-a/
    - project/services/service-a/
    - project/backend/service-a/
    """
    results = {}

    IGNORE_DIRS = [
        '.git', 'target', 'node_modules',
        'venv', '__pycache__', '.github',
        'client', 'frontend', 'ui', 'web',
        'docker', 'docs', 'k8s', 'scripts',
        'uploads', 'resources', 'test', 'tests',
        'infrastructure', 'terraform', 'ansible',
        'libs', 'lib', 'common', 'shared'
    ]

    def scan_directory(path, depth=0):
        if depth > 3:
            return

        try:
            items = os.listdir(path)
        except Exception:
            return

        for item in items:
            item_path = os.path.join(path, item)

            if not os.path.isdir(item_path):
                continue

            if item in IGNORE_DIRS:
                continue

            # C'est un vrai microservice ?
            if is_microservice(item_path):
                result = count_endpoints_from_java(item_path)
                if result["total"] > 0:
                    results[item] = result
            else:
                # Pas un service → descendre d'un niveau
                scan_directory(item_path, depth + 1)

    scan_directory(project_path)
    return results