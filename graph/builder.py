import networkx as nx

def build_graph(services):
    """
    Construit un graphe dirigé de dépendances
    à partir des services parsés.
    
    Noeud  = un service
    Arête  = une dépendance (A → B signifie A dépend de B)
    """
    
    G = nx.DiGraph()
    
    # Ajouter tous les services comme noeuds
    for service_name in services:
        G.add_node(service_name)
    
    # Ajouter les dépendances comme arêtes
    for service_name, config in services.items():
        depends_on = config.get("depends_on", [])
        
        for dependency in depends_on:
            # Vérifier que la dépendance est un service connu
            if dependency in services:
                G.add_edge(service_name, dependency)
    
    return G