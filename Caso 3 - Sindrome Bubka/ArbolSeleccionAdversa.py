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


def crear_arbol_decision():
    raiz = NodoDecision("Inicio", tipo='decision')

    contrato_asimetrico = NodoDecision("Contrato basado en\n información asimétrica", tipo='decision')
    raiz.agregar_hijo(contrato_asimetrico, etiqueta_arista='Opción 1')

    seleccion_adversa = NodoDecision(
        "Alta probabilidad de seleccionar\n un socio de bajo rendimiento\n (Selección Adversa)", tipo='terminal')
    riesgo_futuro = NodoDecision("Mayor rentabilidad en el corto plazo,\n pero con alto riesgo de problemas futuros",
                                 tipo='terminal')
    contrato_asimetrico.agregar_hijo(seleccion_adversa, etiqueta_arista='Alta probabilidad')
    contrato_asimetrico.agregar_hijo(riesgo_futuro, etiqueta_arista='Alto riesgo')

    contrato_simetrico = NodoDecision("Contrato basado en\n información simétrica", tipo='decision')
    raiz.agregar_hijo(contrato_simetrico, etiqueta_arista='Opción 2')

    menor_riesgo = NodoDecision(
        "Menor riesgo de selección adversa,\n mayor probabilidad de seleccionar un socio adecuado", tipo='terminal')
    menor_rentabilidad = NodoDecision(
        "Menor rentabilidad\n en el corto plazo\n debido a los costos de obtener\n información adicional",
        tipo='terminal')
    contrato_simetrico.agregar_hijo(menor_riesgo, etiqueta_arista='Menor riesgo')
    contrato_simetrico.agregar_hijo(menor_rentabilidad, etiqueta_arista='Menor rentabilidad')

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

        plt.title("Seleccion adversa", fontsize=20)
        plt.axis("off")
        plt.tight_layout()

        plt.savefig(f"arbol_decision_paso_{i}.png", dpi=300, bbox_inches="tight")
        frames.append(imageio.imread(f"arbol_decision_paso_{i}.png"))

    imageio.mimsave("arbol_decision_contrato.gif", frames, duration=1)
    print("GIF guardado como arbol_decision_contrato.gif")


# Crear y dibujar el árbol
arbol_decision = crear_arbol_decision()
dibujar_arbol_paso_a_paso(arbol_decision)
#  P(t) = P0 + k * log(t + 1)

