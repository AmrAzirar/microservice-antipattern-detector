import networkx as nx
from detectors.base import BaseDetector

class CyclicDepsDetector(BaseDetector):
    
    def get_name(self):
        return "Cyclic Dependencies"
    
    def detect(self, graph):
        """
        Détecte les dépendances cycliques dans le graphe.
        Exemple : A → B → C → A
        """
        
        violations = []
        
        # NetworkX détecte tous les cycles en 1 ligne
        cycles = list(nx.simple_cycles(graph))
        
        if cycles:
            for cycle in cycles:
                # Reformater le cycle pour l'affichage
                # [A, B, C] → "A → B → C → A"
                cycle_str = " → ".join(cycle) + f" → {cycle[0]}"
                
                violations.append({
                    "type":     "Cyclic Dependencies",
                    "severity": "CRITICAL",
                    "cycle":    cycle,
                    "services": cycle,
                    "message":  f"Cycle détecté : {cycle_str}"
                })
        
        return violations