from detectors.god_service import GodServiceDetector

detector = GodServiceDetector()
violations = detector.detect("datasets/ground-truth")

print("\n" + "="*50)
print("   RÉSULTATS — GOD SERVICE")
print("="*50)

if violations:
    for v in violations:
        if v["severity"] == "CRITICAL":
            print(f"\n🔴 CRITICAL — {v['type']}")
        else:
            print(f"\n🟡 WARNING  — {v['type']}")
        print(f"   Service    : {v['services']}")
        print(f"   Endpoints  : {v['nb_endpoints']}")
        print(f"   Message    : {v['message']}")
else:
    print("\n✅ Aucun God Service détecté")

print("="*50)