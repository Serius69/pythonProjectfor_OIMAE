import networkx as nx
import matplotlib.pyplot as plt

def create_extensive_form_game():
    G = nx.DiGraph()

    # Nodo raíz (decisión del sindicato)
    G.add_node("Root", pos=(0, 0))

    wages = [2700, 3000]  # Posibles demandas salariales

    for i, w in enumerate(wages):
        # Nodos de decisión de la empresa
        node_w = f"w={w}"
        G.add_node(node_w, pos=(-1 + i, -.5))
        G.add_edge("Root", node_w, label=f"w={w}")

        # Calcular L óptimo
        L_opt = (10 - w) / 1

        # Nodos de resultado
        node_result = f"w={w},L={L_opt:.2f}"
        G.add_node(node_result, pos=(-1 + i, -1))
        G.add_edge(node_w, node_result, label=f"L={L_opt:.2f}")

    return G

# Crear el gráfico
G = create_extensive_form_game()

# Dibujar el gráfico
pos = nx.get_node_attributes(G, 'pos')
plt.figure(figsize=(8, 6))
nx.draw(G, pos, with_labels=False, node_size=3000, node_color="lightblue")
nx.draw_networkx_labels(G, pos, {node: node for node in G.nodes() if node != "Root"})
nx.draw_networkx_labels(G, pos, {node: G.nodes[node]['label'] for node in G.nodes() if 'label' in G.nodes[node]})

edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

plt.title("Juego de Negociación en Forma Extensiva")
plt.axis('off')
plt.tight_layout()

# Guardar el gráfico
plt.savefig("extensive_form_game2.png", dpi=300, bbox_inches='tight')
print("Gráfico guardado como extensive_form_game.png")