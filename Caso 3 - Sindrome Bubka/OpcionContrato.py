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

def crear_arbol_bubka():
    # Nodo raíz: Decisión de cómo establecer incentivos para mitigar el Síndrome de Bubka.
    raiz = NodoDecision("Inicio: Cómo establecer incentivos\npara mitigar el Síndrome de Bubka", tipo='decision')

    # Opción 1: Incentivos por mejoras incrementales constantes.
    incentivos_incrementales = NodoDecision("Incentivos por mejoras\n incrementales constantes", tipo='decision')
    raiz.agregar_hijo(incentivos_incrementales)

    # Nodo 1: Implementar un Sistema de Incentivos por Progresos Parciales
    progresos_parciales = NodoDecision("Sistema de Incentivos\npor Progresos Parciales", tipo='decision')
    incentivos_incrementales.agregar_hijo(progresos_parciales)

    # Resultado 1.1: Recompensas por avances parciales
    recompensas_parciales = NodoDecision("Recompensas por \navances parciales", tipo='decision')
    progresos_parciales.agregar_hijo(recompensas_parciales)

    # Nodo 1.1.1: Incluir Evaluaciones de Rendimiento Frecuentes
    evaluaciones_frecuentes = NodoDecision("Evaluaciones de Rendimiento\nFrecuentes", tipo='decision')
    recompensas_parciales.agregar_hijo(evaluaciones_frecuentes)

    # Resultado 1.1.1.1: Feedback regular y ajustes necesarios
    feedback_regular = NodoDecision("Feedback regular y\najustes necesarios", tipo='terminal')
    evaluaciones_frecuentes.agregar_hijo(feedback_regular)

    # Nodo 1.1.2: Aplicar Penalizaciones por Retrasos Injustificados
    penalizaciones_retrasos = NodoDecision("Penalizaciones por Retrasos\nInjustificados", tipo='decision')
    recompensas_parciales.agregar_hijo(penalizaciones_retrasos)

    # Resultado 1.1.2.1: Disuade la procrastinación
    disuade_procrastinacion = NodoDecision("Disuade la \nprocrastinación", tipo='terminal')
    penalizaciones_retrasos.agregar_hijo(disuade_procrastinacion)

    # Resultado 1.2: Estímulo constante para mejoras
    estimulo_mejoras = NodoDecision("Estímulo constante \npara mejoras", tipo='decision')
    incentivos_incrementales.agregar_hijo(estimulo_mejoras)

    # Nodo 1.2.1: Establecer Criterios de Evaluación Claros
    criterios_claros = NodoDecision("Criterios de \nEvaluación Claros", tipo='decision')
    estimulo_mejoras.agregar_hijo(criterios_claros)

    # Resultado 1.2.1.1: Medición precisa del progreso
    medicion_progreso = NodoDecision("Medición precisa\n del progreso", tipo='terminal')
    criterios_claros.agregar_hijo(medicion_progreso)

    # Nodo 1.2.2: Incluir Capacitación y Recursos
    capacitacion_recursos = NodoDecision("Capacitación y Recursos", tipo='decision')
    estimulo_mejoras.agregar_hijo(capacitacion_recursos)

    # Resultado 1.2.2.1: Mejora en la capacidad para cumplir objetivos
    mejora_capacidad = NodoDecision("Mejora en la capacidad\npara cumplir objetivos", tipo='terminal')
    capacitacion_recursos.agregar_hijo(mejora_capacidad)

    # Opción 2: Incentivos por logros significativos pero menos frecuentes
    incentivos_significativos = NodoDecision("Incentivos por logros\nsignificativos pero\n menos frecuentes", tipo='decision')
    raiz.agregar_hijo(incentivos_significativos)

    # Nodo 2: Implementar un Sistema de Incentivos por Logros Significativos
    logros_significativos = NodoDecision("Sistema de Incentivos\npor Logros Significativos", tipo='decision')
    incentivos_significativos.agregar_hijo(logros_significativos)

    # Resultado 2.1: Recompensas por logros grandes
    recompensas_grandes = NodoDecision("Recompensas por \nlogros grandes", tipo='terminal')
    logros_significativos.agregar_hijo(recompensas_grandes)

    # Nodo 2.1.1: Definir Logros Significativos
    definir_logros = NodoDecision("Definir Logros \nSignificativos", tipo='decision')
    recompensas_grandes.agregar_hijo(definir_logros)

    # Resultado 2.1.1.1: Claridad en lo que se considera un gran logro
    claridad_logros = NodoDecision("Claridad en lo que se considera\nun gran logro", tipo='terminal')
    definir_logros.agregar_hijo(claridad_logros)

    # Nodo 2.1.2: Establecer Penalizaciones por Intentos de Manipulación
    penalizaciones_manipulacion = NodoDecision("Penalizaciones por Intentos\nde Manipulación", tipo='decision')
    recompensas_grandes.agregar_hijo(penalizaciones_manipulacion)

    # Resultado 2.1.2.1: Reducción del riesgo de retraso intencionado (Síndrome de Bubka)
    reduccion_riesgo = NodoDecision("Reducción del riesgo de retraso\nintencionado (Síndrome de Bubka)", tipo='terminal')
    penalizaciones_manipulacion.agregar_hijo(reduccion_riesgo)

    # Resultado 2.2: Estímulo para la innovación
    estimulo_innovacion = NodoDecision("Estímulo para \nla innovación", tipo='terminal')
    incentivos_significativos.agregar_hijo(estimulo_innovacion)

    # Nodo 2.2.1: Implementar un Plan de Acción Detallado
    plan_accion = NodoDecision("Plan de Acción Detallado", tipo='decision')
    estimulo_innovacion.agregar_hijo(plan_accion)

    # Resultado 2.2.1.1: Direccionamiento claro para alcanzar logros
    direccionamiento_logros = NodoDecision("Direccionamiento claro\npara alcanzar logros", tipo='terminal')
    plan_accion.agregar_hijo(direccionamiento_logros)

    # Nodo 2.2.2: Establecer Mecanismos de Retroalimentación
    mecanismos_retroalimentacion = NodoDecision("Mecanismos de\n Retroalimentación", tipo='decision')
    estimulo_innovacion.agregar_hijo(mecanismos_retroalimentacion)

    # Resultado 2.2.2.1: Feedback para mantener la motivación
    feedback_motivacion = NodoDecision("Feedback para \nmantener la motivación", tipo='terminal')
    mecanismos_retroalimentacion.agregar_hijo(feedback_motivacion)

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
    G, pos = crear_grafo(arbol, espaciado_x=4, espaciado_y=2)

    plt.figure(figsize=(30, 30))

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
    nx.draw_networkx_labels(G, pos, labels, font_size=20, font_weight="bold")

    plt.title("Árbol de Decisión: Planteamiento de Incentivos", fontsize=60)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("arbol_buencontrato.png", dpi=300, bbox_inches="tight")
    plt.show()
    print("Gráfico del árbol de decisión guardado como arbol_buencontrato.png")

# Crear y dibujar el árbol
arbol_incentivos = crear_arbol_bubka()
dibujar_arbol(arbol_incentivos)
