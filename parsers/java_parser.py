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


def count_endpoints_from_java(service_path):
    """
    Compte les endpoints depuis les annotations
    Spring Boot dans les fichiers Java
    Parcourt récursivement tous les sous-dossiers
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

        # Ignorer dossiers non pertinents
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

                # Analyser seulement les Controllers
                if not is_controller_file(content):
                    continue

                # Compter les endpoints
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
    Trouve tous les services Java dans le projet
    Parcourt récursivement pour trouver
    les controllers à n'importe quelle profondeur
    Retourne : dict service_name → résultat
    """
    results = {}

    # Parcourir les dossiers directs = services
    try:
        items = os.listdir(project_path)
    except Exception:
        return results

    for item in items:
        service_path = os.path.join(project_path, item)

        if not os.path.isdir(service_path):
            continue

        # Ignorer dossiers non pertinents
        if item in ['.git', 'target', 'node_modules',
                    'venv', '__pycache__', '.github',
                    'datasets', 'report', 'tests']:
            continue

        # Chercher controllers dans tout le sous-arbre
        result = count_endpoints_from_java(service_path)

        if result["total"] > 0:
            results[item] = result

    return results