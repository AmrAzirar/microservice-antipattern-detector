# Antipattern Detector

Outil CLI Python d'analyse statique d'architectures microservices. Il détecte automatiquement les anti-patterns architecturaux à partir des fichiers de configuration d'un projet (Docker Compose, OpenAPI, fichiers source).

---

## Anti-patterns détectés

| Anti-pattern | Sévérité | Source analysée |
|---|---|---|
| **Shared Database** | CRITICAL | `docker-compose.yml` |
| **Cyclic Dependencies** | CRITICAL | `docker-compose.yml` |
| **God Service** | WARNING / CRITICAL | `openapi.yaml` / `swagger.yaml` |
| **Hardcoded Endpoints** | CRITICAL | Fichiers source (`.java`, `.py`, `.js`, `.properties`, `.yml`, `.env`, `.conf`) |

---

## Architecture

```
antipattern-detector/
├── main.py                    # Point d'entrée CLI
├── parsers/
│   ├── docker_compose.py      # Parse docker-compose.yml → services + dépendances
│   └── openapi.py             # Parse openapi.yaml → liste d'endpoints
├── graph/
│   └── builder.py             # Construit un graphe dirigé (NetworkX DiGraph)
├── detectors/
│   ├── base.py                # Classe abstraite BaseDetector
│   ├── shared_db.py           # Détecte plusieurs services sur la même DB
│   ├── cyclic_deps.py         # Détecte les cycles dans le graphe de dépendances
│   ├── god_service.py         # Détecte les services avec trop d'endpoints
│   └── hardcoded_endpoints.py # Détecte les URLs/IPs/ports écrits en dur
├── report/
│   └── generator.py           # Générateur de rapport (en cours)
├── tests/                     # Scripts de test manuels par détecteur
└── datasets/
    ├── ecommerce/             # Dataset e-commerce de test
    └── ground-truth/          # Dataset de référence avec anti-patterns intentionnels
```

---

## Fonctionnement

Le pipeline d'analyse suit 4 étapes :

```
1. PARSE    → Lecture docker-compose.yml + fichiers OpenAPI
2. GRAPH    → Construction du graphe de dépendances (NetworkX)
3. DETECT   → Exécution de chaque détecteur
4. REPORT   → Affichage des violations + Quality Gate
```

Si aucun `docker-compose.yml` n'est trouvé, les détecteurs Shared Database et Cyclic Dependencies sont ignorés. Le détecteur God Service et Hardcoded Endpoints fonctionnent de manière indépendante.

---

## Installation

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux / macOS

pip install pyyaml networkx jinja2
```

---

## Utilisation

```bash
python main.py --path <chemin/vers/le/projet>
```

**Exemple :**

```bash
python main.py --path datasets/ground-truth
```

**Sortie typique :**

```
=======================================================
   DÉTECTEUR D'ANTI-PATTERNS MICROSERVICES
=======================================================

📂 Projet analysé : datasets/ground-truth
✅ Parser OK — 7 services détectés
✅ Graphe construit — 9 dépendances

📊 Détection en cours...

=======================================================
   RÉSULTATS
=======================================================

🔴 CRITICAL — Shared Database
   Services : ['authentication-service', 'common-data-service', 'payment-service']
   Message  : 3 services partagent la même base : mysql-db/${DB_SCHEMA}

=======================================================
❌ Quality Gate FAILED — 1 anti-pattern(s) critique(s)
=======================================================
```

---

## Quality Gate

L'outil retourne un **code de sortie** utilisable en CI/CD :

| Code | Signification |
|---|---|
| `0` | Aucun anti-pattern critique — Quality Gate PASSED |
| `1` | Au moins un anti-pattern CRITICAL — Quality Gate FAILED |

---

## Détails des détecteurs

### Shared Database
Détecte plusieurs services partageant la même base de données (même `DB_HOST` + `DB_SCHEMA` dans les variables d'environnement Docker).

### Cyclic Dependencies
Construit un graphe orienté à partir des `depends_on` Docker Compose, puis détecte les cycles via `networkx.simple_cycles()`.

### God Service
Analyse les fichiers `openapi.yaml` / `swagger.yaml` et compte les endpoints HTTP. Seuils configurables dans `god_service.py` :
- `WARNING_THRESHOLD = 10` endpoints
- `CRITICAL_THRESHOLD = 15` endpoints

### Hardcoded Endpoints
Scan par regex des fichiers source pour détecter les URLs écrites en dur. Trois patterns :
- IP hardcodée : `http://192.168.x.x:port`
- Localhost hardcodé : `http://localhost:port/path`
- Port hardcodé : `http://hostname:port`

Une whitelist évite les faux positifs (`${...}`, `example.com`, commentaires, `localhost:8080`).

---

## Datasets de test

- `datasets/ground-truth/` — projet de référence avec anti-patterns intentionnels :
  - `docker-compose.yml` : 3 services sur la même DB (`mysql-db`) → Shared Database CRITICAL
  - `hardcoded-example.properties` : URLs IP et localhost en dur
  - `auth-service/openapi.yaml` et `common-data-service/openapi.yaml` : specs OpenAPI pour tester God Service

---

## Dépendances

| Package | Usage |
|---|---|
| `pyyaml` | Parsing des fichiers YAML |
| `networkx` | Graphe de dépendances + détection de cycles |
| `jinja2` | Génération de rapports (à venir) |
