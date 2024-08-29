import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def calculate_payoffs(w, L):
    """Calcula los pagos para el sindicato y la empresa."""
    U = w * L  # Utilidad del sindicato
    pi = 3850 * L - 2.5 * L ** 2 - w * L  # Beneficio de la empresa (ajustado para números más grandes)
    return U, pi


def optimal_L(w):
    """Calcula el L óptimo para un w dado."""
    print(f"  w = {w:.0f}")
    return (3850 - w) / 5  # Ajustado para la nueva función de beneficio


def create_extensive_form_game():
    G = nx.DiGraph()

    # Nodo raíz (decisión del sindicato)
    G.add_node("Root", pos=(0, 0))

    wages = [2700, 3000]  # Demandas salariales

    for i, w in enumerate(wages):
        # Nodos de decisión de la empresa
        node_w = f"w={w}"
        G.add_node(node_w, pos=(-0.5 + i, -.5))
        G.add_edge("Root", node_w, label=f"w={w}")

        # Calcular L óptimo
        L_opt = optimal_L(w)

        # Nodos de resultado
        L_values = [L_opt * .9, L_opt * 1.1]  # Dos opciones alrededor del óptimo
        for j, L in enumerate(L_values):
            node_result = f"w={w},L={L:.0f}"
            G.add_node(node_result, pos=(-0.75 + i + j * .5, -1))
            G.add_edge(node_w, node_result, label=f"L={L:.0f}")

            # Calcular pagos
            U, pi = calculate_payoffs(w, L)
            G.nodes[node_result]['label'] = f"U={U / 1e6:.2f}M\n\nπ={pi / 1e6:.2f}M"

    return G


# Crear el gráfico
G = create_extensive_form_game()

# Dibujar el gráfico
pos = nx.get_node_attributes(G, 'pos')
plt.figure(figsize=(12, 8))
nx.draw(G, pos, with_labels=False, node_size=3000, node_color="lightblue")
nx.draw_networkx_labels(G, pos, {node: node for node in G.nodes() if node != "Root"})
nx.draw_networkx_labels(G, pos, {node: G.nodes[node]['label'] for node in G.nodes() if 'label' in G.nodes[node]})

edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

plt.title("Juego de Negociación en Forma Extensiva")
plt.axis('off')
plt.tight_layout()

# Guardar el gráfico
plt.savefig("extensive_form_game.png", dpi=600, bbox_inches='tight')
print("Gráfico guardado como extensive_form_game.png")

# Mostrar los cálculos
print("\nCálculos realizados:")
for w in [2700, 3000]:
    L_opt = optimal_L(w)
    print(f"\nPara w = {w}:")
    print(f"  L óptimo = {L_opt:.0f}")
    for L in [L_opt * .9, L_opt * 1.1]:
        U, pi = calculate_payoffs(w, L)
        print(f"  Si L = {L:.0f}:\n\n   U = {U / 1e6:.2f} M\n\n\n   π = {pi / 1e6:.2f} M")
