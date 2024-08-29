import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar
import networkx as nx


class EmpresaLicitadora:
    def __init__(self, nombre, costo_bajo, costo_alto, prob_costo_bajo):
        self.nombre = nombre
        self.costo_bajo = costo_bajo
        self.costo_alto = costo_alto
        self.prob_costo_bajo = prob_costo_bajo

    def costo_esperado(self):
        return self.prob_costo_bajo * self.costo_bajo + (1 - self.prob_costo_bajo) * self.costo_alto

    def utilidad_esperada(self, oferta, prob_ganar):
        return (oferta - self.costo_esperado()) * prob_ganar


def prob_ganar(oferta, otras_ofertas):
    return np.mean(oferta < otras_ofertas)


def simular_licitacion(empresas, num_iteraciones=5):
    historial_ofertas = {empresa.nombre: [] for empresa in empresas}
    historial_utilidades = {empresa.nombre: [] for empresa in empresas}
    arbol_decision = nx.DiGraph()

    def simular_ronda(nodo_padre, profundidad, max_profundidad):
        if profundidad == max_profundidad:
            return

        ofertas_actuales = {}
        for empresa in empresas:
            otras_ofertas = [e.costo_esperado() for e in empresas if e != empresa]

            def negativo_utilidad_esperada(x):
                return -empresa.utilidad_esperada(x, prob_ganar(x, otras_ofertas))

            resultado = minimize_scalar(negativo_utilidad_esperada, bounds=(empresa.costo_bajo, empresa.costo_alto * 2),
                                        method='bounded')
            oferta_optima = resultado.x

            ofertas_actuales[empresa.nombre] = oferta_optima
            historial_ofertas[empresa.nombre].append(oferta_optima)

            utilidad = empresa.utilidad_esperada(oferta_optima, prob_ganar(oferta_optima, otras_ofertas))
            historial_utilidades[empresa.nombre].append(utilidad)

        nodo_actual = f"Ronda {profundidad}"
        arbol_decision.add_edge(nodo_padre, nodo_actual)
        for empresa, oferta in ofertas_actuales.items():
            nodo_empresa = f"{empresa}: {oferta:.2f}"
            arbol_decision.add_edge(nodo_actual, nodo_empresa)
            simular_ronda(nodo_empresa, profundidad + 1, max_profundidad)

    simular_ronda("Inicio", 0, num_iteraciones)

    return historial_ofertas, historial_utilidades, arbol_decision


def graficar_resultados(historial_ofertas, historial_utilidades, arbol_decision):
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 24))

    for empresa, ofertas in historial_ofertas.items():
        ax1.plot(ofertas, label=f'Ofertas de {empresa}')
    ax1.set_title('Evolución de las Ofertas')
    ax1.set_xlabel('Iteración')
    ax1.set_ylabel('Monto de la Oferta')
    ax1.legend()

    for empresa, utilidades in historial_utilidades.items():
        ax2.plot(utilidades, label=f'Utilidad de {empresa}')
    ax2.set_title('Evolución de las Utilidades Esperadas')
    ax2.set_xlabel('Iteración')
    ax2.set_ylabel('Utilidad Esperada')
    ax2.legend()

    pos = nx.spring_layout(arbol_decision, k=0.9, iterations=50)
    nx.draw(arbol_decision, pos, ax=ax3, with_labels=True, node_color='lightblue',
            node_size=3000, font_size=8, font_weight='bold', arrows=True)
    nx.draw_networkx_labels(arbol_decision, pos, ax=ax3, font_size=8)
    ax3.set_title('Árbol de Decisión de la Licitación')

    plt.tight_layout()
    plt.show()


# Configuración de las empresas
empresa_a = EmpresaLicitadora("Empresa A", costo_bajo=80, costo_alto=120, prob_costo_bajo=0.6)
empresa_b = EmpresaLicitadora("Empresa B", costo_bajo=90, costo_alto=110, prob_costo_bajo=0.5)

# Simulación
historial_ofertas, historial_utilidades, arbol_decision = simular_licitacion([empresa_a, empresa_b])

# Visualización
graficar_resultados(historial_ofertas, historial_utilidades, arbol_decision)

# Resultados finales
print("Resultados finales:")
for empresa in [empresa_a, empresa_b]:
    ofertas = historial_ofertas[empresa.nombre]
    utilidades = historial_utilidades[empresa.nombre]
    print(f"{empresa.nombre}:")
    print(f"  Oferta promedio: {np.mean(ofertas):.2f}")
    print(f"  Utilidad esperada promedio: {np.mean(utilidades):.2f}")