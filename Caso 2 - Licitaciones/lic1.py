import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple

def generar_datos_ejemplo() -> Tuple[List[str], List[float], List[float]]:
    """
    Genera datos de ejemplo para las licitaciones de carreteras.
    Retorna una tupla con años, datos de Brasil y datos de Chile.
    """
    años = [str(year) for year in range(2015, 2025)]
    datos_brasil = np.random.rand(10) * 100  # Valores aleatorios entre 0 y 100
    datos_chile = np.random.rand(10) * 100
    return años, list(datos_brasil), list(datos_chile)

def generar_diagrama_barras(años: List[str], datos_brasil: List[float], datos_chile: List[float]) -> None:
    """
    Genera un diagrama de barras comparando las licitaciones de Brasil y Chile.
    """
    x = np.arange(len(años))
    width = 0.35

    fig, ax = plt.subplots(figsize=(12, 6))
    rects1 = ax.bar(x - width/2, datos_brasil, width, label='Brasil', color='green')
    rects2 = ax.bar(x + width/2, datos_chile, width, label='Chile', color='red')

    ax.set_ylabel('Valor de licitaciones (Millones USD)')
    ax.set_title('Comparación de licitaciones de carreteras: Brasil vs Chile')
    ax.set_xticks(x)
    ax.set_xticklabels(años)
    ax.legend()

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    fig.tight_layout()
    plt.savefig('comparacion_licitaciones_barras.png')
    plt.close()

def generar_diagrama_lineas(años: List[str], datos_brasil: List[float], datos_chile: List[float]) -> None:
    """
    Genera un diagrama de líneas comparando las licitaciones de Brasil y Chile.
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(años, datos_brasil, marker='o', linestyle='-', color='green', label='Brasil')
    ax.plot(años, datos_chile, marker='s', linestyle='--', color='red', label='Chile')

    ax.set_xlabel('Año')
    ax.set_ylabel('Valor de licitaciones (Millones USD)')
    ax.set_title('Tendencia de licitaciones de carreteras: Brasil vs Chile')
    ax.legend()

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('comparacion_licitaciones_lineas.png')
    plt.close()

def main():
    años, datos_brasil, datos_chile = generar_datos_ejemplo()
    generar_diagrama_barras(años, datos_brasil, datos_chile)
    generar_diagrama_lineas(años, datos_brasil, datos_chile)
    print("Diagramas generados: 'comparacion_licitaciones_barras.png' y 'comparacion_licitaciones_lineas.png'")

if __name__ == "__main__":
    main()