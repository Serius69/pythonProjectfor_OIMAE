import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class EmpresaLicitadora:
    def __init__(self, id, costo_base, experiencia):
        self.id = id
        self.costo_base = costo_base
        self.experiencia = experiencia
        self.historial_ofertas = []

    def calcular_oferta(self, factores_externos):
        eficiencia = np.random.normal(1, 0.1)  # Factor de eficiencia interno
        impacto_externo = sum(factores_externos.values())
        oferta = self.costo_base * eficiencia * (1 + impacto_externo) * (1 - self.experiencia * 0.01)
        self.historial_ofertas.append(oferta)
        return oferta


class SimuladorLicitaciones:
    def __init__(self, num_empresas, num_iteraciones):
        self.empresas = [EmpresaLicitadora(i, np.random.uniform(800000, 1200000), np.random.uniform(0, 10))
                         for i in range(num_empresas)]
        self.num_iteraciones = num_iteraciones
        self.historial_ganadores = []
        self.historial_ofertas_ganadoras = []

    def simular_factores_externos(self):
        return {
            'inflacion': np.random.normal(0.02, 0.01),
            'politica_economica': np.random.uniform(-0.05, 0.05),
            'condiciones_mercado': np.random.uniform(-0.03, 0.03)
        }

    def realizar_licitacion(self):
        factores_externos = self.simular_factores_externos()
        ofertas = [empresa.calcular_oferta(factores_externos) for empresa in self.empresas]
        ganador = np.argmin(ofertas)
        self.historial_ganadores.append(ganador)
        self.historial_ofertas_ganadoras.append(ofertas[ganador])

        # Actualizar experiencia del ganador
        self.empresas[ganador].experiencia += 0.5

    def ejecutar_simulacion(self):
        for _ in range(self.num_iteraciones):
            self.realizar_licitacion()

    def visualizar_resultados(self):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

        # Gráfico de ofertas por empresa
        for empresa in self.empresas:
            ax1.plot(empresa.historial_ofertas, label=f'Empresa {empresa.id}')
        ax1.set_title('Evolución de Ofertas por Empresa')
        ax1.set_xlabel('Iteración')
        ax1.set_ylabel('Monto de Oferta')
        ax1.legend()

        # Gráfico de ganadores y montos ganadores
        scatter = ax2.scatter(range(self.num_iteraciones), self.historial_ofertas_ganadoras,
                              c=self.historial_ganadores, cmap='viridis')
        ax2.set_title('Ofertas Ganadoras por Iteración')
        ax2.set_xlabel('Iteración')
        ax2.set_ylabel('Monto de Oferta Ganadora')
        plt.colorbar(scatter, ax=ax2, label='ID de Empresa Ganadora')

        plt.tight_layout()
        plt.show()

    def animar_evolucion(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        lines = [ax.plot([], [], label=f'Empresa {i}')[0] for i in range(len(self.empresas))]

        ax.set_xlim(0, self.num_iteraciones)
        ax.set_ylim(min([min(e.historial_ofertas) for e in self.empresas]) * 0.9,
                    max([max(e.historial_ofertas) for e in self.empresas]) * 1.1)
        ax.set_title('Evolución Dinámica de Ofertas')
        ax.set_xlabel('Iteración')
        ax.set_ylabel('Monto de Oferta')
        ax.legend()

        def update(frame):
            for line, empresa in zip(lines, self.empresas):
                line.set_data(range(frame + 1), empresa.historial_ofertas[:frame + 1])
            return lines

        anim = FuncAnimation(fig, update, frames=self.num_iteraciones, blit=True, interval=200)
        plt.show()


# Ejecutar la simulación
simulador = SimuladorLicitaciones(num_empresas=5, num_iteraciones=50)
simulador.ejecutar_simulacion()
simulador.visualizar_resultados()
simulador.animar_evolucion()