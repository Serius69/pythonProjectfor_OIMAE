import networkx as nx
import matplotlib.pyplot as plt


def create_centipede_game():
    G = nx.DiGraph()

    # Añadir nodos
    nodes = [
        ("Start", {"player": "S", "payoffs": None}),
        ("1,1", {"player": "P", "payoffs": (1, 1)}),
        ("0,3", {"player": "P", "payoffs": (0, 3)}),
        ("2,2", {"player": "P", "payoffs": (2, 2)}),
        ("97,100", {"player": "P", "payoffs": (97, 100)}),
        ("99,99", {"player": "P", "payoffs": (99, 99)}),
        ("98,101", {"player": "P", "payoffs": (98, 101)}),
        ("End", {"player": "S", "payoffs": (100, 100)})
    ]
    G.add_nodes_from(nodes)

    # Añadir aristas
    edges = [
        ("Start", "1,1"), ("Start", "0,3"),
        ("0,3", "2,2"), ("0,3", "97,100"),
        ("97,100", "99,99"), ("97,100", "98,101"),
        ("98,101", "End")
    ]
    G.add_edges_from(edges)

    return G


def plot_centipede_game(G):
    pos = {
        "Start": (0, 0), "1,1": (1, -1), "0,3": (2, 0),
        "2,2": (3, -1), "97,100": (4, 0), "99,99": (5, -1),
        "98,101": (6, 0), "End": (7, 0)
    }

    plt.figure(figsize=(15, 5))
    nx.draw(G, pos, with_labels=False, node_color='lightblue', node_size=3000, arrowsize=20)

    # Añadir etiquetas a los nodos
    labels = {}
    for node in G.nodes(data=True):
        if node[1]['payoffs']:
            labels[node[0]] = f"{node[0]}\n{node[1]['player']}\n{node[1]['payoffs']}"
        else:
            labels[node[0]] = f"{node[0]}\n{node[1]['player']}"

    nx.draw_networkx_labels(G, pos, labels, font_size=8)

    # Añadir etiquetas a las aristas
    edge_labels = {
        ("Start", "1,1"): "S", ("Start", "0,3"): "C",
        ("0,3", "2,2"): "S", ("0,3", "97,100"): "C",
        ("97,100", "99,99"): "S", ("97,100", "98,101"): "C",
        ("98,101", "End"): "C"
    }
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8)

    plt.title("El juego del ciempiés (Centipede Game)")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('centipede_game.png', dpi=300, bbox_inches='tight')
    plt.show()


# Crear y visualizar el juego
G = create_centipede_game()
plot_centipede_game(G)