from detectors.hardcoded_endpoints import HardcodedEndpointsDetector

detector = HardcodedEndpointsDetector()
violations = detector.detect("datasets/ground-truth")

print("\n" + "="*50)
print("   RÉSULTATS — HARDCODED ENDPOINTS")
print("="*50)

if violations:
    for v in violations:
        print(f"\n🔴 CRITICAL — {v['type']}")
        print(f"   Message : {v['message']}")
        print(f"\n   Détails :")
        for f in v['findings']:
            print(f"   📄 {f['file']}")
            print(f"      Ligne {f['line_num']} : {f['url']}")
            print(f"      Type  : {f['pattern_type']}")
else:
    print("\n✅ Aucun endpoint hardcodé détecté")

print("="*50)