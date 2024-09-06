import networkx as nx
import matplotlib.pyplot as plt

class NodoDecision:
    def __init__(self, nombre, tipo='decision', payoff='', ecuacion=''):
        self.nombre = nombre
        self.tipo = tipo  # 'decision', 'chance', o 'terminal'
        self.hijos = []
        self.payoff = payoff
        self.ecuacion = ecuacion

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)

def crear_arbol_incentivos():
    # Nodo raíz: Decisión de cómo plantear los incentivos.
    raiz = NodoDecision("Inicio", tipo='decision')

    # Opción 1: Incentivos por mejoras incrementales constantes.
    incentivos_incrementales = NodoDecision("Incentivos por mejoras\n incrementales constantes", tipo='decision')
    raiz.agregar_hijo(incentivos_incrementales)

    # Nodo 1: Si se elige Incentivos por mejoras incrementales constantes
    mejora_constante = NodoDecision("Estímulo para mejoras constantes,\n pero riesgo de aprovechar el sistema", tipo='terminal')
    desmotivacion_mejora = NodoDecision("Desmotivación si las mejoras\n no son valoradas correctamente", tipo='terminal')
    incentivos_incrementales.agregar_hijo(mejora_constante)
    incentivos_incrementales.agregar_hijo(desmotivacion_mejora)

    # Opción 2: Incentivos por logros significativos pero menos frecuentes.
    incentivos_significativos = NodoDecision("Incentivos por logros\n significativos pero menos frecuentes", tipo='decision')
    raiz.agregar_hijo(incentivos_significativos)

    # Nodo 2: Si se elige Incentivos por logros significativos pero menos frecuentes
    innovacion_grande = NodoDecision("Estímulo para grandes innovaciones,\n pero riesgo de retrasar logros\n intencionadamente (Síndrome de Bubka)", tipo='terminal')
    desmotivacion_dificultad = NodoDecision("Posible desmotivación si los logros\n significativos son difíciles de alcanzar", tipo='terminal')
    incentivos_significativos.agregar_hijo(innovacion_grande)
    incentivos_significativos.agregar_hijo(desmotivacion_dificultad)

    return raiz

def crear_grafo(nodo, G=None, pos=None, x=0, y=0, espaciado_x=1, espaciado_y=1, parent=None):
    if G is None:
        G = nx.DiGraph()
        pos = {}

    G.add_node(nodo.nombre, pos=(x, y), tipo=nodo.tipo, ecuacion=nodo.ecuacion, payoff=nodo.payoff)
    pos[nodo.nombre] = (x, y)

    if parent:
        G.add_edge(parent.nombre, nodo.nombre)

    num_hijos = len(nodo.hijos)
    ancho_nivel = (num_hijos - 1) * espaciado_x
    for i, hijo in enumerate(nodo.hijos):
        nuevo_x = x - ancho_nivel / 2 + i * espaciado_x
        nuevo_y = y - espaciado_y
        crear_grafo(hijo, G, pos, nuevo_x, nuevo_y, espaciado_x / 2, espaciado_y, nodo)

    return G, pos

def dibujar_arbol(arbol):
    G, pos = crear_grafo(arbol, espaciado_x=8, espaciado_y=2)

    plt.figure(figsize=(50, 36))

    # Dibujar nodos
    node_colors = {'decision': 'lightblue', 'chance': 'lightgreen', 'terminal': 'lightcoral'}
    node_shapes = {'decision': 's', 'chance': 'o', 'terminal': 'd'}

    for tipo in node_colors:
        node_list = [node for node in G.nodes() if G.nodes[node]['tipo'] == tipo]
        nx.draw_networkx_nodes(G, pos, nodelist=node_list, node_color=node_colors[tipo],
                               node_size=3000, node_shape=node_shapes[tipo])

    # Dibujar aristas
    nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, arrowsize=20)

    # Añadir etiquetas
    labels = {node: f"{node}\n{G.nodes[node]['ecuacion']}\n{G.nodes[node]['payoff']}"
              for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=40, font_weight="bold")

    plt.title("Árbol de Decisión: Planteamiento de Incentivos", fontsize=60)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("arbol_decision_incentivos.png", dpi=1200, bbox_inches="tight")
    plt.show()
    print("Gráfico del árbol de decisión guardado como arbol_decision_incentivos.png")

# Crear y dibujar el árbol
arbol_incentivos = crear_arbol_incentivos()
dibujar_arbol(arbol_incentivos)
