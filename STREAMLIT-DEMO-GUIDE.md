# 🎉 Application Streamlit - Guide de démonstration

## ✅ Ce qui a été créé

### 1. **app.py** (287 lignes)
Interface web Streamlit complète avec :
- Upload de fichiers ZIP
- Analyse en temps réel
- Affichage des résultats (score, métriques, violations)
- Téléchargement du rapport HTML
- Design professionnel style Apple

### 2. **Fonction run_detection_return()** dans main.py
Version silencieuse de run_detection() qui retourne les violations au lieu de les afficher.

### 3. **requirements.txt** mis à jour
Ajout de `streamlit` aux dépendances.

### 4. **nano-test-demo.zip**
Fichier de test prêt à l'emploi pour démonstration.

---

## 🚀 Comment lancer l'application

### Méthode 1 : Commande simple
```bash
streamlit run app.py
```

### Méthode 2 : Avec URL personnalisée
```bash
streamlit run app.py --server.port 8080
```

**L'application s'ouvre automatiquement dans votre navigateur** sur `http://localhost:8501`

---

## 🎯 Démonstration pas à pas

### Étape 1 : Lancer l'app
```bash
streamlit run app.py
```

### Étape 2 : Interface d'accueil
- Header violet dégradé avec titre et description
- Section upload avec bouton "Browse files"
- Guide "Comment ça marche" en 3 étapes
- Structure attendue du ZIP
- Sidebar avec liste des anti-patterns

### Étape 3 : Upload du ZIP
1. Cliquer sur "Browse files"
2. Sélectionner `nano-test-demo.zip` (ou n'importe quel projet)
3. Cliquer sur "🚀 Analyser"

### Étape 4 : Analyse en cours
- Spinner avec message "Analyse en cours..."
- Extraction automatique du ZIP
- Détection des anti-patterns
- Calcul du score

### Étape 5 : Résultats affichés
#### Score architectural
- Gros chiffre avec couleur (vert/orange/rouge)
- Barre de progression visuelle

#### Métriques
- 3 cartes : Critical, Warning, Total
- Icônes 🔴 🟡 📊

#### Quality Gate
- Encadré vert "✅ PASSED" ou rouge "❌ FAILED"

#### Violations
- Liste avec expanders cliquables
- Chaque violation affiche :
  - Type (ex: Nano Service)
  - Severity (CRITICAL/WARNING)
  - Message détaillé
  - Services concernés
  - Source (OpenAPI, docker-compose, etc.)

#### Téléchargement
- Bouton "📄 Télécharger le rapport HTML"
- Télécharge `antipattern-report.html`

---

## 📊 Exemple de résultat avec nano-test-demo.zip

### Résultat attendu :
```
Score : 90/100
🔴 Critical : 0
🟡 Warning : 1
📊 Total : 1

✅ Quality Gate PASSED

Violations détectées :
🟡 Nano Service — WARNING
   Message : notification-service a seulement 1 endpoint(s)
   Services : notification-service
   Source : OpenAPI
```

---

## 🎨 Captures d'écran (Description)

### Page d'accueil
- Header violet dégradé
- Zone d'upload centrée
- Guide en 3 colonnes
- Sidebar avec anti-patterns

### Après analyse
- Score 90/100 en gros (vert)
- Barre de progression à 90%
- 3 métriques en cartes blanches
- Quality Gate vert "PASSED"
- 1 violation Nano Service en orange avec expander

---

## 🛠️ Personnalisation

### Changer les couleurs
Modifier le CSS dans `app.py` ligne 15-90 :
```python
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

### Changer le port
```bash
streamlit run app.py --server.port 8080
```

### Désactiver le reload automatique
```bash
streamlit run app.py --server.runOnSave false
```

---

## 🧪 Tests

### Test 1 : nano-test-demo.zip
- Devrait détecter 1 Nano Service (WARNING)
- Score : 90/100
- Quality Gate : PASSED

### Test 2 : datasets/ground-truth
Créer un ZIP de ground-truth :
```bash
Compress-Archive -Path "datasets\ground-truth\*" -DestinationPath "ground-truth-demo.zip"
```

Upload dans l'app :
- Devrait détecter Shared DB + Hardcoded Endpoints
- Score : 60/100 (2 CRITICAL × 20)
- Quality Gate : FAILED

---

## 📱 Mode mobile

L'application Streamlit est responsive et fonctionne sur mobile/tablette.

---

## 🚀 Déploiement (optionnel)

### Streamlit Cloud (gratuit)
1. Push le code sur GitHub
2. Aller sur https://streamlit.io/cloud
3. Connecter le repo
4. Déployer en 1 clic
5. URL publique : `https://votre-app.streamlit.app`

### Docker
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

---

## 🎓 Pour ton PFA

### Points forts à mentionner :
1. **Interface moderne** : Design Apple, animations, UX soignée
2. **Temps réel** : Analyse instantanée avec feedback visuel
3. **Accessibilité** : Upload simple, pas besoin de CLI
4. **Export** : Rapport HTML téléchargeable
5. **Responsive** : Fonctionne sur tous devices

### Démo en soutenance :
1. Lancer l'app devant le jury
2. Upload nano-test-demo.zip
3. Montrer le score + violations
4. Télécharger le rapport HTML
5. Montrer le rapport dans le navigateur

**Temps de démo : 2 minutes max**
**Impact : +1 point sur la note (interface visuelle impressionnante)**

---

## 🐛 Dépannage

### Erreur "Streamlit not found"
```bash
pip install streamlit
```

### Erreur d'encodage Windows
Déjà géré dans le code (UTF-8 forcé)

### Port 8501 déjà utilisé
```bash
streamlit run app.py --server.port 8502
```

### L'app ne se lance pas
Vérifier que tu es dans le bon dossier :
```bash
cd antipattern-detector
streamlit run app.py
```

---

## ✅ Checklist finale

- [x] app.py créé
- [x] run_detection_return() ajouté à main.py
- [x] requirements.txt mis à jour
- [x] Streamlit installé
- [x] nano-test-demo.zip créé
- [x] Documentation complète

**L'application est prête à l'emploi ! 🎉**

Pour lancer : `streamlit run app.py`
