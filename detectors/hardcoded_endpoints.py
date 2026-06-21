import re
import os
import ast
from detectors.base import BaseDetector

class HardcodedEndpointsDetector(BaseDetector):

    # Patterns d'URLs hardcodées à détecter
    PATTERNS = [
        (r'http://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(:\d+)?',
         "IP hardcodée"),
        (r'http://localhost(:\d+)?/\w+',
         "localhost hardcodé"),
        (r'http://[a-zA-Z0-9\-]+:\d{4,5}(?!/\$)',
         "Port hardcodé"),
    ]

    # Fichiers à analyser
    EXTENSIONS = [
        '.java', '.py', '.js',
        '.properties', '.yml',
        '.yaml', '.env', '.conf'
    ]

    # Ignorer ces patterns (faux positifs)
    WHITELIST = [
        '${',           # variables Spring
        'example.com',  # URLs d'exemple
        '#',            # commentaires
        'schema.org',   # schemas
        'localhost:8080' # port dev standard
    ]

    def get_name(self):
        return "Hardcoded Endpoints"

    def is_whitelisted(self, url):
        """Vérifie si l'URL doit être ignorée"""
        return any(w in url for w in self.WHITELIST)

    def matches_url_pattern(self, text):
        """Vérifie si le texte correspond à un pattern d'URL hardcodée"""
        if not isinstance(text, str):
            return None
        for pattern, pattern_name in self.PATTERNS:
            if re.search(pattern, text):
                return pattern_name
        return None

    def parse_python_file(self, filepath):
        """Parse un fichier Python avec AST"""
        urls = []
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                code = f.read()
            tree = ast.parse(code, filename=filepath)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Constant) and isinstance(node.value, str):
                    pattern_type = self.matches_url_pattern(node.value)
                    if pattern_type and not self.is_whitelisted(node.value):
                        urls.append((node.lineno, node.value.strip('"\''), pattern_type))
        except:
            pass
        return urls

    def parse_java_file(self, filepath):
        """Parse un fichier Java avec javalang"""
        urls = []
        try:
            import javalang
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                code = f.read()
            tree = javalang.parse.parse(code)
            
            for path, node in tree:
                if isinstance(node, javalang.tree.Literal):
                    if node.value:
                        value = node.value.strip('"')
                        pattern_type = self.matches_url_pattern(value)
                        if pattern_type and not self.is_whitelisted(value):
                            urls.append((node.position.line if node.position else 0, value, pattern_type))
        except:
            pass
        return urls

    def parse_config_file_regex(self, filepath):
        """Parse fichiers de config avec regex (fallback)"""
        urls = []
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            for line_num, line in enumerate(lines, 1):
                stripped = line.strip()
                if stripped.startswith(('#', '//', '*', '/*')):
                    continue
                
                for pattern, pattern_name in self.PATTERNS:
                    matches = re.finditer(pattern, line)
                    for match in matches:
                        url = match.group()
                        if not self.is_whitelisted(url):
                            urls.append((line_num, url, pattern_name))
        except:
            pass
        return urls

    def is_comment(self, line):
        """Vérifie si la ligne est un commentaire"""
        stripped = line.strip()
        return stripped.startswith(('//', '#', '*', '/*'))

    def get_service_name(self, filepath, project_path):
        """
        Retourne le nom du vrai service parent
        en remontant jusqu'au microservice
        """
        from parsers.java_parser import is_microservice

        path = os.path.dirname(filepath)

        while path != project_path and \
              path != os.path.dirname(path):
            if is_microservice(path):
                return os.path.basename(path)
            path = os.path.dirname(path)

        # Fallback
        return os.path.basename(os.path.dirname(filepath))

    def detect(self, project_path):
        findings = []

        for root, dirs, files in os.walk(project_path):

            # Ignorer les dossiers non pertinents
            dirs[:] = [d for d in dirs
                if d not in [
                    'node_modules', '.git',
                    'target', 'venv',
                    '__pycache__', '.idea',
                    'resources', 'config',    
                    'static', 'templates',
                    'META-INF', 'webapp'
                ]]

            for filename in files:
                ext = os.path.splitext(filename)[1]
                if ext not in self.EXTENSIONS:
                    continue

                # Ignorer les fichiers de test
                if 'test' in filename.lower():
                    continue

                filepath = os.path.join(root, filename)
                urls = []

                # Parser avec AST pour les fichiers code
                if ext == '.py':
                    urls = self.parse_python_file(filepath)
                elif ext == '.java':
                    urls = self.parse_java_file(filepath)
                # Parser avec regex pour les fichiers config
                elif ext in ['.properties', '.yml', '.yaml', '.env', '.conf', '.js']:
                    urls = self.parse_config_file_regex(filepath)

                # Ajouter les findings
                for line_num, url, pattern_type in urls:
                    findings.append({
                        "file":         filepath,
                        "line_num":     line_num,
                        "url":          url,
                        "pattern_type": pattern_type,
                        "service":      self.get_service_name(filepath, project_path)
                    })

        # Construire les violations
        violations = []

        if findings:
            services = list(set(f["service"] for f in findings))

            violations.append({
                "type":     "Hardcoded Endpoints",
                "severity": "CRITICAL",
                "services": services,
                "findings": findings,
                "message":  f"{len(findings)} endpoint(s) hardcodé(s) détecté(s) dans {len(services)} service(s)"
            })

        return violations