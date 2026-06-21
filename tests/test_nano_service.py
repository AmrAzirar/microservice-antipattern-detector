"""
Test unitaire pour le détecteur Nano Service
"""
from detectors.nano_service import NanoServiceDetector


def test_nano_service_detection():
    """
    Test sur le dataset nano-test
    - notification-service : 1 endpoint → WARNING
    - user-service : 5 endpoints → OK
    """
    detector = NanoServiceDetector()
    violations = detector.detect("datasets/nano-test")
    
    print(f"\nViolations detectees : {len(violations)}")
    
    # Doit détecter 1 nano service
    assert len(violations) == 1, f"Attendu 1 violation, recu {len(violations)}"
    
    # Vérifier que c'est notification-service
    v = violations[0]
    assert v["type"] == "Nano Service"
    assert v["severity"] == "WARNING"
    assert "notification-service" in v["services"]
    
    print(f"   Service : {v['services'][0]}")
    print(f"   Message : {v['message']}")
    print("\nTest Nano Service reussi !")


if __name__ == "__main__":
    test_nano_service_detection()
