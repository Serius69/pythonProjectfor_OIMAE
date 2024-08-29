import networkx as nx
import matplotlib.pyplot as plt

def create_extensive_form_game():
    G = nx.DiGraph()

    # Nodo raíz (decisión del sindicato)
    G.add_node("Root", pos=(0, 0))

    wages = [2500, 2700]  # Salario mínimo actual y propuesta del sindicato

    for i, w in enumerate(wages):
        # Nodos de decisión de la empresa
        node_w = f"w={w}"
        G.add_node(node_w, pos=(-1 + i*2, -0.5))
        G.add_edge("Root", node_w, label=f"w={w}")

        # Calcular L óptimo
        L_opt = (3850 - w) / 5  # Derivado de la Etapa 2 en la imagen

        # Calcular beneficio
        R = 3850 * L_opt - 2.5 * L_opt**2
        profit = R - w * L_opt

        # Nodos de resultado
        node_result = f"w={w}\nL={L_opt:.2f}\nπ={profit:.2f}"
        G.add_node(node_result, pos=(-1 + i*2, -1))
        G.add_edge(node_w, node_result, label=f"L={L_opt:.2f}")

    return G

# Crear el gráfico
G = create_extensive_form_game()

# Dibujar el gráfico
pos = nx.get_node_attributes(G, 'pos')
plt.figure(figsize=(12, 8))
nx.draw(G, pos, with_labels=False, node_size=5000, node_color="lightblue")
nx.draw_networkx_labels(G, pos, {node: node for node in G.nodes() if node != "Root"})

edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

plt.title("Juego de Negociación Sindicato-Empresa en Forma Extensiva")
plt.axis('off')
plt.tight_layout()

# Guardar el gráfico
plt.savefig("extensive_form_game_case_study.png", dpi=300, bbox_inches='tight')
print("Gráfico guardado como extensive_form_game_case_study.png")