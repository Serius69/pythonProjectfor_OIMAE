import networkx as nx
import matplotlib.pyplot as plt
import imageio


class NodoDecision:
    def __init__(self, nombre, tipo='decision', payoff='', ecuacion=''):
        self.nombre = nombre
        self.tipo = tipo  # 'decision', 'chance', o 'terminal'
        self.hijos = []
        self.payoff = payoff
        self.ecuacion = ecuacion

    def agregar_hijo(self, hijo, etiqueta_arista=''):
        self.hijos.append((hijo, etiqueta_arista))


def crear_arbol_decision_riesgo_moral():
    raiz = NodoDecision("Inicio", tipo='decision')

    contrato_sin_incentivos = NodoDecision("Contrato sin\nincentivos", tipo='decision')
    raiz.agregar_hijo(contrato_sin_incentivos, etiqueta_arista='Opción 1')

    bajo_esfuerzo = NodoDecision("Alta probabilidad de\nbajo esfuerzo del agente", tipo='terminal')
    resultados_suboptimos = NodoDecision("Resultados subóptimos\npara el principal", tipo='terminal')
    contrato_sin_incentivos.agregar_hijo(bajo_esfuerzo, etiqueta_arista='Alta probabilidad')
    contrato_sin_incentivos.agregar_hijo(resultados_suboptimos, etiqueta_arista='Resultados subóptimos')

    contrato_con_incentivos = NodoDecision("Contrato con\nincentivos", tipo='decision')
    raiz.agregar_hijo(contrato_con_incentivos, etiqueta_arista='Opción 2')

    alto_esfuerzo = NodoDecision("Mayor probabilidad de\nalto esfuerzo del agente", tipo='terminal')
    mayores_costos = NodoDecision("Mayores costos para\nel principal debido a\nlos incentivos", tipo='terminal')
    contrato_con_incentivos.agregar_hijo(alto_esfuerzo, etiqueta_arista='Mayor probabilidad')
    contrato_con_incentivos.agregar_hijo(mayores_costos, etiqueta_arista='Mayores costos')

    return raiz


def crear_grafo(nodo, G=None, pos=None, x=0, y=0, espaciado_x=1, espaciado_y=1, parent=None, etiquetas_aristas=None):
    if G is None:
        G = nx.DiGraph()
        pos = {}
        etiquetas_aristas = {}

    G.add_node(nodo.nombre, pos=(x, y), tipo=nodo.tipo, ecuacion=nodo.ecuacion, payoff=nodo.payoff)
    pos[nodo.nombre] = (x, y)

    if parent:
        etiqueta_arista = nodo.hijos[-1][1] if nodo.hijos else ''
        G.add_edge(parent.nombre, nodo.nombre)
        etiquetas_aristas[(parent.nombre, nodo.nombre)] = etiqueta_arista

    num_hijos = len(nodo.hijos)
    ancho_nivel = (num_hijos - 1) * espaciado_x
    for i, (hijo, _) in enumerate(nodo.hijos):
        nuevo_x = x - ancho_nivel / 2 + i * espaciado_x
        nuevo_y = y - espaciado_y
        crear_grafo(hijo, G, pos, nuevo_x, nuevo_y, espaciado_x / 2, espaciado_y, nodo, etiquetas_aristas)

    return G, pos, etiquetas_aristas


def dibujar_arbol_paso_a_paso(arbol):
    G, pos, etiquetas_aristas = crear_grafo(arbol, espaciado_x=8, espaciado_y=2)

    plt.figure(figsize=(10, 6))
    node_colors = {'decision': 'lightblue', 'chance': 'lightgreen', 'terminal': 'lightcoral'}
    node_shapes = {'decision': 's', 'chance': 'o', 'terminal': 'd'}

    frames = []
    for i in range(1, len(G.edges()) + 1):
        plt.clf()
        subG = G.edge_subgraph(list(G.edges())[:i]).copy()

        for tipo in node_colors:
            node_list = [node for node in subG.nodes() if G.nodes[node]['tipo'] == tipo]
            nx.draw_networkx_nodes(G, pos, nodelist=node_list, node_color=node_colors[tipo],
                                   node_size=3000, node_shape=node_shapes[tipo])

        nx.draw_networkx_edges(subG, pos, edge_color='gray', arrows=True, arrowsize=20)
        nx.draw_networkx_edge_labels(subG, pos, edge_labels={key: etiquetas_aristas[key] for key in subG.edges()},
                                     font_color='red')
        labels = {node: f"{node}\n{G.nodes[node]['ecuacion']}\n{G.nodes[node]['payoff']}"
                  for node in subG.nodes()}
        nx.draw_networkx_labels(G, pos, labels, font_size=6, font_weight="bold")

        plt.title("Riesgo Moral", fontsize=20)
        plt.axis("off")
        plt.tight_layout()

        plt.savefig(f"arbol_decision_paso_{i}.png", dpi=300, bbox_inches="tight")
        frames.append(imageio.imread(f"arbol_decision_riesgo_moral_{i}.png"))

    imageio.mimsave("arbol_decision_riesgo_moral.gif", frames, duration=1)
    print("GIF guardado como arbol_decision_riesgo_moral.gif")


# Crear y dibujar el árbol
arbol_decision_riesgo_moral = crear_arbol_decision_riesgo_moral()
dibujar_arbol_paso_a_paso(arbol_decision_riesgo_moral)