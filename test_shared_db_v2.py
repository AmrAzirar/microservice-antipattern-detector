from detectors.shared_db import SharedDbDetector
from parsers.properties_parser import find_db_configs

# Debug — voir ce que le parser trouve
print("\n🔍 DEBUG — Recherche des fichiers config...")
configs = find_db_configs("datasets/ground-truth")

print(f"\nFichiers trouvés : {len(configs)}")
for service, info in configs.items():
    print(f"  Service : {service}")
    print(f"  DB Host : {info.get('db_host')}")
    print(f"  DB Schema : {info.get('db_schema')}")

# Test détection
detector = SharedDbDetector()
violations = detector.detect_from_configs("datasets/ground-truth")

print("\n" + "="*55)
print("   RÉSULTATS — SHARED DB (config files)")
print("="*55)

if violations:
    for v in violations:
        print(f"\n🔴 {v['severity']} — {v['type']}")
        print(f"   Source   : {v['source']}")
        print(f"   Base     : {v['database']}")
        print(f"   Services : {v['services']}")
else:
    print("\n✅ Aucun Shared Database détecté")

print("="*55)