import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


class NodoDecision:
    def __init__(self, nombre, tipo='decision', payoff=None, ecuacion=None):
        self.nombre = nombre
        self.tipo = tipo  # 'decision', 'chance', o 'terminal'
        self.hijos = []
        self.payoff = payoff
        self.ecuacion = ecuacion

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)


def crear_arbol_licitaciones_complejo():
    # Nodo raíz
    raiz = NodoDecision("G", tipo='decision')
    n = 3  # Número de empresas

    # Nivel 1: Decisión de licitación pública o privada
    ln_pub = NodoDecision("Inversion Publica", tipo='decision')
    ln_priv = NodoDecision("Inversion Privada", tipo='decision')
    raiz.agregar_hijo(ln_pub)
    raiz.agregar_hijo(ln_priv)

    # Nivel 2: Estrategia de oferta para licitación pública
    in_prop = NodoDecision("Inversion Propia", tipo='decision')
    pre_intern = NodoDecision("Prestamo Interno", tipo='decision')
    ln_pub.agregar_hijo(in_prop)
    ln_pub.agregar_hijo(pre_intern)

    # Nivel 2: Estrategia de oferta para licitación privada (para cada empresa)
    probabilidades_empresas = [
        {"Calidad Buena": 0.5, "Calidad Neutral": 0.5},
        {"Calidad Buena": 0.6, "Calidad Neutral": 0.4},
        {"Calidad Buena": 0.7, "Calidad Neutral": 0.3}
    ]

    for i in range(1, n + 1):
        empresa_n = NodoDecision(f"Empresa {i}", tipo='decision')
        ln_priv.agregar_hijo(empresa_n)

        # Nivel 3: Escenarios de calidad (nodos de azar) para cada empresa
        probabilidades = probabilidades_empresas[i - 1]

        for escenario, prob in probabilidades.items():
            nodo_calidad = NodoDecision(f"{escenario} ({i})", tipo='chance', ecuacion=f"P={prob}")
            empresa_n.agregar_hijo(nodo_calidad)

            # Nivel 4: Resultado único para cada nodo de calidad
            # resultado = NodoDecision(f"Resultado \n({escenario}, \nEmpresa {i})", tipo='terminal')
            resultado = NodoDecision(f"Resultado \n({escenario} - \n{'Gana' if prob > 0.5 else 'No Gana'})", tipo='terminal')
            nodo_calidad.agregar_hijo(resultado)

            # Añadir ecuaciones y payoffs para el resultado
            # resultado.ecuacion = f"UE = {prob} * ((p_{i} - c_{i}) * q - CF_{i} - R_{i}(p_{i}))"
            resultado.payoff = ""

    return raiz

def crear_grafo_juego_extensivo(nodo, G=None, pos=None, x=0, y=0, nivel=0, parent=None, espaciado_x=1, espaciado_y=1):
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
        crear_grafo_juego_extensivo(hijo, G, pos, nuevo_x, nuevo_y, nivel + 1, nodo, espaciado_x / 2, espaciado_y)

    return G, pos


def dibujar_arbol_licitaciones_complejo(arbol):
    G, pos = crear_grafo_juego_extensivo(arbol, espaciado_x=8, espaciado_y=2)

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
    labels = {}
    for node in G.nodes():
        label = node
        if G.nodes[node]['ecuacion']:
            label += f"\n{G.nodes[node]['ecuacion']}"
        if G.nodes[node]['payoff']:
            label += f"\nPayoff: {G.nodes[node]['payoff']}"
        labels[node] = label

    nx.draw_networkx_labels(G, pos, labels, font_size=8, font_weight="bold")

    plt.title("Modelo Bolivia Licitaciones Bolivia", fontsize=16)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("modelo_arbol.png", dpi=300, bbox_inches="tight")
    print("Gráfico del modelo complejo guardado como modelo_arbol.png")


# Crear y dibujar el árbol
arbol_licitaciones_complejo = crear_arbol_licitaciones_complejo()
dibujar_arbol_licitaciones_complejo(arbol_licitaciones_complejo)


def calcular_resultados(estrategias, escenarios, probabilidades_empresas):
    resultados = []
    for i, estrategia in enumerate(estrategias, start=1):
        for escenario, prob in probabilidades_empresas[i - 1].items():
            # Parámetros simulados (estos deberían ser ajustados según datos reales)
            p_i = 100 if estrategia == "Agresiva" else 120  # Precio ofertado
            c_i = 80  # Costo marginal
            q = 1000  # Cantidad demandada
            CF_i = 5000  # Costos fijos

            # Cálculo de la probabilidad de ganar ajustada por el escenario
            P_ganar = prob
            if escenario == "Calidad Buena":
                P_ganar += 0.1
            elif escenario == "Calidad Neutral":
                P_ganar -= 0.1

            # Asegurar que la probabilidad esté en el rango [0, 1]
            P_ganar = max(0, min(1, P_ganar))

            # Cálculo del factor de riesgo (simplificado)
            R_i = 2000 if estrategia == "Agresiva" else 1000

            # Cálculo de la Utilidad Esperada
            UE = P_ganar * (p_i - c_i) * q - CF_i - R_i

            resultados.append({
                "Empresa": i,
                "Estrategia": estrategia,
                "Escenario": escenario,
                "P(ganar)": P_ganar,
                "UE": UE
            })

    return pd.DataFrame(resultados)


def mostrar_tabla_resultados(df_resultados):
    plt.figure(figsize=(12, 6))
    plt.axis('off')
    plt.title("Tabla de Resultados de las Ecuaciones", fontsize=16)

    tabla = plt.table(cellText=df_resultados.values,
                      colLabels=df_resultados.columns,
                      cellLoc='center',
                      loc='center')

    tabla.auto_set_font_size(False)
    tabla.set_fontsize(10)
    tabla.scale(1.2, 1.5)

    plt.tight_layout()
    plt.savefig("tabla_resultados_licitaciones.png", dpi=300, bbox_inches="tight")
    print("Tabla de resultados Licitaciones Bolivia.png")


# Función principal
def analisis_licitaciones_completo():
    # Crear y dibujar el árbol
    arbol_licitaciones_complejo = crear_arbol_licitaciones_complejo()
    dibujar_arbol_licitaciones_complejo(arbol_licitaciones_complejo)

    # Calcular y mostrar los resultados en una tabla
    estrategias = ["Agresiva", "Conservadora"]
    escenarios = ["Favorable", "Neutral", "Desfavorable"]
    probabilidades_empresas = [
        {"Calidad Buena": 0.5, "Calidad Neutral": 0.5},
        {"Calidad Buena": 0.6, "Calidad Neutral": 0.4},
        {"Calidad Buena": 0.7, "Calidad Neutral": 0.3}
    ]
    df_resultados = calcular_resultados(estrategias, escenarios,probabilidades_empresas)
    mostrar_tabla_resultados(df_resultados)

    # Imprimir los resultados en la consola
    print("\nResultados de las ecuaciones:")
    print(df_resultados.to_string(index=False))


# Ejecutar el análisis completo
analisis_licitaciones_completo()