import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

# Datos del problema
proveedores = ['A', 'B', 'C']
porcentajes_compra = [0.5, 0.3, 0.2]
porcentajes_defectuosos = [0.05, 0.07, 0.10]

# Cálculo de probabilidades
P_D = sum(p_c * p_d for p_c, p_d in zip(porcentajes_compra, porcentajes_defectuosos))
print(P_D)
P_A_given_D = (porcentajes_compra[0] * porcentajes_defectuosos[0]) / P_D
print(P_A_given_D)
# Cálculo para todos los proveedores
P_given_D = [(p_c * p_d) / P_D for p_c, p_d in zip(porcentajes_compra, porcentajes_defectuosos)]
print(P_given_D)
# Crear el gráfico
fig, ax = plt.subplots(figsize=(10, 6))

# Graficar barras
bars = ax.bar(proveedores, P_given_D, color=['red', 'green', 'blue'])

# Personalizar el gráfico
ax.set_ylabel('Probabilidad')
ax.set_title('Probabilidad de que un insumo defectuoso provenga de cada proveedor')
ax.set_ylim(0, 1)  # Establecer el límite del eje y de 0 a 1

# Añadir etiquetas de porcentaje en las barras
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.2%}',
            ha='center', va='bottom')

# Añadir una leyenda con los porcentajes originales
legend_labels = [f'{p}: {pc:.0%} compra, {pd:.0%} defectuosos' for p, pc, pd in zip(proveedores, porcentajes_compra, porcentajes_defectuosos)]
ax.legend(bars, legend_labels, title='Proveedores', loc='upper right')

# Mostrar el resultado numérico
print(f"La probabilidad de que el insumo defectuoso se haya comprado del proveedor A es: {P_A_given_D:.2%}")

# Guardar y mostrar el gráfico
plt.tight_layout()
plt.savefig('probabilidad_proveedores.png')
plt.show()

def create_decision_tree():
    G = nx.DiGraph()
    # Nodo raíz
    G.add_node("Inicio", pos=(0, 0))
    # Niveles del árbol
    y_levels = [0, -1, -2]
    x_positions = [-1, 0, 1]
    for i, (proveedor, p_compra, p_defectuoso) in enumerate(
            zip(proveedores, porcentajes_compra, porcentajes_defectuosos)):
        # Nodo del proveedor
        nodo_proveedor = f"Proveedor {proveedor}"
        G.add_node(nodo_proveedor, pos=(x_positions[i], y_levels[1]))
        G.add_edge("Inicio", nodo_proveedor, label=f"{p_compra:.0%}")

        # Nodos de resultado (defectuoso o no)
        nodo_defectuoso = f"{proveedor} Defectuoso"
        nodo_no_defectuoso = f"{proveedor} No Defectuoso"

        G.add_node(nodo_defectuoso, pos=(x_positions[i] - 0.3, y_levels[2]))
        G.add_node(nodo_no_defectuoso, pos=(x_positions[i] + 0.3, y_levels[2]))

        G.add_edge(nodo_proveedor, nodo_defectuoso, label=f"{p_defectuoso:.0%}")
        G.add_edge(nodo_proveedor, nodo_no_defectuoso, label=f"{1 - p_defectuoso:.0%}")

    return G

# Crear el árbol
G = create_decision_tree()

# Configurar el gráfico
pos = nx.get_node_attributes(G, 'pos')
plt.figure(figsize=(12, 8))
nx.draw(G, pos, with_labels=True, node_color='lightblue',
        node_size=3000, font_size=8, font_weight='bold')

# Añadir etiquetas a las aristas
edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# Personalizar el gráfico
plt.title("Árbol de Decisión: Selección de Proveedor y Probabilidad de Defecto")
plt.axis('off')

# Guardar y mostrar el gráfico
plt.tight_layout()
plt.savefig('arbol_decision_proveedores.png', dpi=300, bbox_inches='tight')
plt.show()

# Calcular y mostrar la probabilidad condicional
P_D = sum(p_c * p_d for p_c, p_d in zip([0.5, 0.3, 0.2], [0.05, 0.07, 0.10]))
P_A_given_D = (0.5 * 0.05) / P_D

print(f"La probabilidad de que el insumo defectuoso se haya comprado del proveedor A es: {P_A_given_D:.2%}")