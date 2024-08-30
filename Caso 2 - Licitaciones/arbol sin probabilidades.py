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


def crear_arbol_licitaciones():
    # Nodo raíz
    raiz = NodoDecision("Inicio", tipo='decision')
    n = 3  # Número de empresas

    # Nivel 1: Decisión de licitación pública o privada
    ln_pub = NodoDecision("Inversión\n Pública", tipo='decision')
    ln_priv = NodoDecision("Inversión\n Privada", tipo='decision')
    raiz.agregar_hijo(ln_pub)
    raiz.agregar_hijo(ln_priv)

    # Nivel 2: Estrategia de oferta para licitación pública
    in_prop = NodoDecision("Inversión\n Propia", tipo='decision')
    pre_intern = NodoDecision("Préstamo\n Internacional", tipo='decision')
    ln_pub.agregar_hijo(in_prop)
    ln_pub.agregar_hijo(pre_intern)

    # Nivel 2: Estrategia de oferta para licitación privada (para cada empresa)
    for i in range(1, n + 1):
        empresa_n = NodoDecision(f"Empresa {i}", tipo='decision')
        ln_priv.agregar_hijo(empresa_n)

        # Nivel 3: Escenarios de calidad (nodos de azar) para cada empresa
        for escenario in ["Calidad\n Buena", "Calidad\n Normal"]:
            nodo_calidad = NodoDecision(f"{escenario} ({i})", tipo='chance')
            empresa_n.agregar_hijo(nodo_calidad)

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

    plt.figure(figsize=(20, 12))

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
    nx.draw_networkx_labels(G, pos, labels, font_size=8, font_weight="bold")

    plt.title("Modelo de Licitaciones", fontsize=16)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("modelo_arbol.png", dpi=300, bbox_inches="tight")
    plt.show()
    print("Gráfico del modelo guardado como modelo_arbol.png")


# Crear y dibujar el árbol
arbol_licitaciones = crear_arbol_licitaciones()
dibujar_arbol(arbol_licitaciones)
