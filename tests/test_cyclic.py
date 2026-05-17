from parsers.docker_compose import parse_docker_compose
from graph.builder import build_graph
from detectors.cyclic_deps import CyclicDepsDetector

# 1. Parser
services = parse_docker_compose("datasets/ecommerce/docker-compose.yml")

# 2. Construire le graphe
graph = build_graph(services)

print(f"✅ Graphe construit")
print(f"   Noeuds : {list(graph.nodes())}")
print(f"   Arêtes : {list(graph.edges())}")

# 3. Détecter les cycles
detector = CyclicDepsDetector()
violations = detector.detect(graph)

print("\n" + "="*50)
if violations:
    for v in violations:
        print(f"🔴 CRITICAL — {v['type']}")
        print(f"   {v['message']}")
else:
    print("✅ Aucun cycle détecté")
print("="*50)


# ─── Test avec un cycle artificiel ───────────────
print("\n🧪 TEST AVEC CYCLE ARTIFICIEL")
print("="*50)

import networkx as nx

# Créer un graphe avec un cycle A → B → C → A
test_graph = nx.DiGraph()
test_graph.add_edge("service-a", "service-b")
test_graph.add_edge("service-b", "service-c")
test_graph.add_edge("service-c", "service-a")  # ← cycle !

violations = detector.detect(test_graph)

if violations:
    for v in violations:
        print(f"🔴 CRITICAL — {v['type']}")
        print(f"   {v['message']}")
else:
    print("✅ Aucun cycle détecté")
print("="*50)