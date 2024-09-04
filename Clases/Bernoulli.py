import networkx as nx
import matplotlib.pyplot as plt
import math

def create_bernoulli_tree(n):
    G = nx.DiGraph()

    # Crear nodos
    for level in range(n + 1):
        for i in range(2 ** level):
            node_id = f"{level}-{i}"
            G.add_node(node_id, level=level)

    # Crear aristas
    for level in range(n):
        for i in range(2 ** level):
            parent = f"{level}-{i}"
            left_child = f"{level + 1}-{2 * i}"
            right_child = f"{level + 1}-{2 * i + 1}"
            G.add_edge(parent, left_child, decision='0')
            G.add_edge(parent, right_child, decision='1')

    return G


def plot_bernoulli_tree(G, n):
    pos = {}
    labels = {}

    # Calcular posiciones de los nodos
    for node, data in G.nodes(data=True):
        level = data['level']
        index = int(node.split('-')[1])
        x = index / (2 ** level - 1) if level > 0 else 0.5
        y = 1 - level / n
        pos[node] = (x, y)

        if level == n:
            binary = format(index, f'0{n}b')
            labels[node] = binary

    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, node_size=1000, node_color='lightblue',
            arrows=True, arrowsize=20, with_labels=False)

    # Dibujar etiquetas solo para los nodos hoja
    nx.draw_networkx_labels(G, pos, labels, font_size=8)

    # Añadir etiquetas a las aristas
    edge_labels = nx.get_edge_attributes(G, 'decision')
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8)

    plt.title(f"Árbol de Decisión de Bernoulli (n={n})")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('bernoulli_tree.png', dpi=300, bbox_inches='tight')
    plt.show()


# Número de decisiones
n = 2  # Puedes cambiar este valor para generar árboles más grandes o pequeños

# Crear y visualizar el árbol
G = create_bernoulli_tree(n)
plot_bernoulli_tree(G, n)

# Imprimir información sobre el árbol
print(f"Número de decisiones: {n}")
print(f"Número total de nodos: {G.number_of_nodes()}")
print(f"Número de resultados posibles: {2 ** n}")