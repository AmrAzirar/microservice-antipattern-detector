# Antipattern Detector - Interface Web Streamlit

Interface web pour analyser et visualiser les anti-patterns architecturaux dans les microservices.

## 🚀 Lancement rapide

```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run app.py
```

L'application s'ouvre automatiquement dans votre navigateur sur `http://localhost:8501`

## 📦 Fonctionnalités

### Upload & Analyse
- Upload d'un fichier ZIP contenant le projet microservices
- Analyse automatique en un clic
- Extraction et nettoyage automatique des fichiers temporaires

### Résultats
- **Score architectural** (0-100) avec barre de progression
- **Métriques** : nombre de violations CRITICAL, WARNING, et total
- **Quality Gate** : PASSED (vert) ou FAILED (rouge)
- **Liste détaillée des violations** avec expanders interactifs

### Rapport
- Téléchargement du rapport HTML complet
- Visualisation dans le navigateur

## 🎨 Design

- Interface propre et professionnelle
- Design inspiré d'Apple (font Inter)
- Animations subtiles au survol
- Code couleur :
  - 🔴 Rouge : CRITICAL
  - 🟡 Orange : WARNING
  - 🟢 Vert : PASSED

## 📋 Structure attendue du ZIP

```
projet-microservices.zip
├── docker-compose.yml          # Détection Shared DB + Cycles
├── service-a/
│   ├── openapi.yaml            # Détection God/Nano Service
│   └── src/
│       └── *.java              # Fallback si pas d'OpenAPI
├── service-b/
│   └── application.properties  # Détection Shared DB
└── *.properties                # Détection Hardcoded Endpoints
```

## 🔍 Anti-patterns détectés

| Anti-pattern | Sévérité | Description |
|---|---|---|
| **Shared Database** | CRITICAL | Plusieurs services partagent la même DB |
| **Cyclic Dependencies** | CRITICAL | Dépendances circulaires entre services |
| **God Service** | CRITICAL | Service avec trop d'endpoints (>15) |
| **Hardcoded Endpoints** | CRITICAL | URLs/IPs écrites en dur dans le code |
| **Nano Service** | WARNING | Service avec trop peu d'endpoints (<3) |

## 🛠️ Technologies

- **Streamlit** : Framework web
- **Python 3.12** : Backend
- **NetworkX** : Analyse de graphes
- **Jinja2** : Génération de rapports

## 📚 Référence scientifique

Basé sur : **Taibi, D., & Lenarduzzi, V. (2020). Microservices Anti-Patterns: A Taxonomy.**

## 🔗 Liens

- [GitHub](https://github.com/AmrAzirar/microservice-antipattern-detector)
- [Documentation CLI](../README.md)
