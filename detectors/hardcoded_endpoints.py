import re
import os
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

    def is_whitelisted(self, line):
        """Vérifie si la ligne doit être ignorée"""
        return any(w in line for w in self.WHITELIST)

    def is_comment(self, line):
        """Vérifie si la ligne est un commentaire"""
        stripped = line.strip()
        return stripped.startswith(('//', '#', '*', '/*'))

    def detect(self, project_path):
        findings = []

        for root, dirs, files in os.walk(project_path):

            # Ignorer les dossiers non pertinents
            dirs[:] = [d for d in dirs
                      if d not in [
                          'node_modules', '.git',
                          'target', 'venv',
                          '__pycache__', '.idea'
                      ]]

            for filename in files:
                ext = os.path.splitext(filename)[1]
                if ext not in self.EXTENSIONS:
                    continue

                filepath = os.path.join(root, filename)

                try:
                    with open(filepath, 'r',
                             encoding='utf-8',
                             errors='ignore') as f:
                        lines = f.readlines()

                    for line_num, line in enumerate(lines, 1):

                        # Ignorer commentaires et whitelist
                        if self.is_comment(line):
                            continue
                        if self.is_whitelisted(line):
                            continue

                        # Vérifier chaque pattern
                        for pattern, pattern_name in self.PATTERNS:
                            matches = re.finditer(pattern, line)
                            for match in matches:
                                url = match.group()
                                findings.append({
                                    "file":         filepath,
                                    "line_num":     line_num,
                                    "url":          url,
                                    "pattern_type": pattern_name,
                                    "service": os.path.basename(
                                        os.path.dirname(filepath)
                                    )
                                })

                except Exception:
                    continue

        # Construire les violations
        violations = []

        if findings:
            # Grouper par service
            services = list(set(f["service"] for f in findings))

            violations.append({
                "type":     "Hardcoded Endpoints",
                "severity": "CRITICAL",
                "services": services,
                "findings": findings,
                "message":  f"{len(findings)} endpoint(s) hardcodé(s) détecté(s) dans {len(services)} service(s)"
            })

        return violations