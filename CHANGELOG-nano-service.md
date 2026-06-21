# Changements - Ajout du détecteur Nano Service

## Date : 21/06/2026

## Résumé
Ajout d'un nouveau détecteur pour identifier les microservices trop petits (< 3 endpoints).

---

## Fichiers créés

### 1. `detectors/nano_service.py` (48 lignes)
- Classe `NanoServiceDetector` héritant de `BaseDetector`
- Détecte les services avec moins de 3 endpoints
- Utilise les mêmes sources que God Service (OpenAPI + annotations Java)
- Seuil configurable : `THRESHOLD = 3`

### 2. `tests/test_nano_service.py` (33 lignes)
- Test unitaire du détecteur
- Utilise le dataset `datasets/nano-test`
- Vérifie la détection de notification-service (1 endpoint)

### 3. `datasets/nano-test/` (dataset de test)
```
nano-test/
├── notification-service/
│   └── openapi.yaml          # 1 endpoint (POST /send-email)
└── user-service/
    └── openapi.yaml          # 5 endpoints (CRUD complet)
```

---

## Fichiers modifiés

### 1. `main.py` (+4 lignes)
- Import : `from detectors.nano_service import NanoServiceDetector`
- Appel : 
```python
nano_violations = NanoServiceDetector().detect(project_path)
all_violations.extend(nano_violations)
```

### 2. `README.md` (+15 lignes)
- Ajout dans le tableau des anti-patterns détectés
- Ajout dans l'arborescence architecture
- Documentation complète du détecteur (section "Nano Service")

---

## Validation

### Test manuel
```bash
python main.py --path datasets/nano-test
```

**Résultat :**
```
🟡 WARNING  — Nano Service
   Services : ['notification-service']
   Message  : notification-service a seulement 1 endpoint(s) — trop petit pour justifier un microservice autonome
```

### Test unitaire
```bash
python tests/test_nano_service.py
```

**Résultat :** ✅ PASS

---

## Impact

- **Avant :** 4 détecteurs (Shared DB, Cyclic Deps, God Service, Hardcoded Endpoints)
- **Après :** 5 détecteurs (+Nano Service)

---

## Notes techniques

### Logique de détection
1. Compte les endpoints via `find_openapi_files()` et `parse_openapi()`
2. Fallback sur annotations Java si pas d'OpenAPI
3. Filtre : `0 < count < THRESHOLD` → WARNING

### Complexité
- Temps : O(n) où n = nombre de services
- Espace : O(n) pour stocker les compteurs

### Limites connues
- Métrique unique (nombre d'endpoints)
- Pas de contexte métier (services utilitaires légitimes)
- Possibles faux positifs sur services spécialisés (notif, email, logger)

### Améliorations futures
- Whitelist pour services utilitaires (`*-notif`, `*-email`, `*-logger`)
- Multi-métriques (LOC + nombre de classes)
- Configuration par projet (`.antipattern-rules.yml`)

---

## Contribution au PFA

Ce nouveau détecteur :
- ✅ Complète God Service (trop petit vs trop gros)
- ✅ Couvre un anti-pattern reconnu dans la littérature
- ✅ Facile à expliquer et mesurer
- ✅ Augmente la valeur de l'outil (4 → 5 patterns)

**Impact attendu sur la note : +0.5 à 1 point**
