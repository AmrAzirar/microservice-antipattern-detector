import argparse
import sys
import os
from parsers.docker_compose import parse_docker_compose
from detectors.shared_db import SharedDbDetector
from detectors.cyclic_deps import CyclicDepsDetector
from graph.builder import build_graph
from detectors.god_service import GodServiceDetector


def parse_args():
    parser = argparse.ArgumentParser(
        description="Détecteur d'anti-patterns architecturaux en microservices"
    )
    parser.add_argument(
        "--path",
        required=True,
        help="Chemin vers le projet à analyser"
    )
    return parser.parse_args()


def find_docker_compose(project_path):
    candidates = [
        os.path.join(project_path, "docker-compose.yml"),
        os.path.join(project_path, "docker-compose.yaml"),
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None


def run_detection(project_path):

    print("\n" + "="*55)
    print("   🔍 DÉTECTEUR D'ANTI-PATTERNS MICROSERVICES")
    print("="*55)

    all_violations = []

    # ─── Étape 1 : Parser ───────────────────────────────
    print(f"\n📂 Projet analysé : {project_path}")

    compose_file = find_docker_compose(project_path)

    if compose_file:
        services = parse_docker_compose(compose_file)
        graph = build_graph(services)
        print(f"✅ Parser OK — {len(services)} services détectés")
        print(f"✅ Graphe construit — {graph.number_of_edges()} dépendances")
    else:
        print("⚠️  Aucun docker-compose.yml — détection DB et cycles ignorée")
        services = {}
        graph = None

    # ─── Étape 2 : Détection ────────────────────────────
    print("\n📊 Détection en cours...\n")

    detectors_list = []

    if services:
        detectors_list.append((SharedDbDetector(), services))

    if graph:
        detectors_list.append((CyclicDepsDetector(), graph))

    detectors_list.append((GodServiceDetector(), project_path))

    for detector, data in detectors_list:
        violations = detector.detect(data)
        all_violations.extend(violations)

    # ─── Étape 3 : Résultats ────────────────────────────
    print("="*55)
    print("   RÉSULTATS")
    print("="*55)

    if all_violations:
        for v in all_violations:
            if v["severity"] == "CRITICAL":
                print(f"\n🔴 CRITICAL — {v['type']}")
            else:
                print(f"\n🟡 WARNING  — {v['type']}")
            print(f"   Services : {v['services']}")
            print(f"   Message  : {v['message']}")
    else:
        print("\n✅ Aucun anti-pattern détecté")

    # ─── Étape 4 : Quality Gate ─────────────────────────
    print("\n" + "="*55)
    criticals = [v for v in all_violations
                 if v["severity"] == "CRITICAL"]

    if criticals:
        print(f"❌ Quality Gate FAILED — {len(criticals)} anti-pattern(s) critique(s)")
        print("="*55 + "\n")
        sys.exit(1)
    else:
        print("✅ Quality Gate PASSED")
        print("="*55 + "\n")
        sys.exit(0)


if __name__ == "__main__":
    args = parse_args()
    run_detection(args.path)