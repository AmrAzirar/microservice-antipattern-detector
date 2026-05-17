from parsers.docker_compose import parse_docker_compose
from detectors.shared_db import SharedDbDetector

# 1. Parser
services = parse_docker_compose("datasets/ecommerce/docker-compose.yml")

# 2. Détecter
detector = SharedDbDetector()
violations = detector.detect(services)

# 3. Afficher les résultats
print("\n" + "="*50)
print("   RÉSULTATS DÉTECTION ANTI-PATTERNS")
print("="*50)

if violations:
    for v in violations:
        print(f"\n🔴 {v['severity']} — {v['type']}")
        print(f"   Base     : {v['database']}")
        print(f"   Services : {v['services']}")
        print(f"   Message  : {v['message']}")
else:
    print("\n✅ Aucun anti-pattern détecté")

print("\n" + "="*50)