import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, interactive, fixed
from ipywidgets import widgets

def revenue_function(L, a=10, b=0.5):
    return a * L - b * L ** 2

def plot_optimal_employment(w_max=10, L_max=10):
    L = np.linspace(0, L_max, 100)
    R = revenue_function(L)

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(L, R, label='R(L)')

    def update(w):
        ax.clear()
        ax.plot(L, R, label='R(L)')
        ax.plot(L, w * L, label=f'wL (w={w:.2f})')

        L_opt = (10 - w) / 1  # Derivada de R(L) igualada a w
        R_opt = revenue_function(L_opt)

        ax.scatter(L_opt, R_opt, color='red', s=100, zorder=5)
        ax.annotate(f'L*(w)={L_opt:.2f}', (L_opt, R_opt), xytext=(5, 5),
                    textcoords='offset points')

        ax.set_xlabel('Empleo (L)')
        ax.set_ylabel('Ingresos (R)')
        ax.set_title('Decisión óptima de empleo de la empresa')
        ax.legend()
        ax.grid(True)

    interact(update, w=widgets.FloatSlider(min=0, max=w_max, step=0.1, value=5))

plot_optimal_employment()


def plot_iso_profit_curves(w_max=3000, L_max=300):
    L = np.linspace(0, L_max, 100)

    fig, ax = plt.subplots(figsize=(10, 6))

    def update(num_curves):
        ax.clear()

        for i in range(num_curves):
            w = np.linspace(0, w_max, 100)
            L_opt = (3850 - w) / 5
            ax.plot(L_opt, w, label=f'Curva {i + 1}')

        ax.set_xlabel('Empleo (L)')
        ax.set_ylabel('Salario (w)')
        ax.set_title('Curvas de isobeneficio de la empresa')
        ax.legend()
        ax.grid(True)

    interact(update, num_curves=widgets.IntSlider(min=1, max=5, step=1, value=3))
# tener los puntos de interaccion

plot_iso_profit_curves()

def plot_inefficient_equilibrium(w_max=3000, L_max=270):
    L = np.linspace(0, L_max, 100)

    fig, ax = plt.subplots(figsize=(10, 6))

    def update(w_star):
        ax.clear()

        L_star = (3850 - w_star) / 5

        # Función de mejor respuesta de la empresa
        w = np.linspace(0, w_max, 100)
        L_opt = (3850 - w) / 5
        ax.plot(L_opt, w, label='L*(w)')

        # Curva de beneficio de la empresa
        w_curve = w_star + (L - L_star) ** 2
        ax.plot(L, w_curve, label='Curva de beneficio')
        # maximizar L*w
        # Punto de equilibrio
        ax.scatter(L_star, w_star, color='red', s=100, zorder=5)
        ax.annotate(f'(L*(w*), w*)=({L_star:.2f}, {w_star:.2f})',
                    (L_star, w_star), xytext=(5, 5), textcoords='offset points')

        # Área sombreada
        idx = (L > L_star) & (w_curve < w_star)
        ax.fill_between(L[idx], w_curve[idx], w_star, alpha=0.3, color='gray')

        ax.set_xlabel('Empleados (L)')
        ax.set_ylabel('Salario (w)')
        ax.set_title('Ineficiencia del equilibrio en la negociación')
        ax.legend()
        ax.grid(True)

    interact(update, w_star=widgets.FloatSlider(min=0, max=w_max, step=0.1, value=5))


plot_inefficient_equilibrium()


def save_optimal_employment_graph(filename='optimal_employment.png', w=5, w_max=10, L_max=300):
    L = np.linspace(0, L_max, 100)
    R = revenue_function(L)

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(L, R, label='R(L)')
    ax.plot(L, w * L, label=f'wL (w={w:.2f})')

    L_opt = (3850 - w) / 5  # Derivada de R(L) igualada a w
    R_opt = revenue_function(L_opt)

    ax.scatter(L_opt, R_opt, color='red', s=100, zorder=5)
    ax.annotate(f'L*(w)={L_opt:.2f}', (L_opt, R_opt), xytext=(5, 5),
                textcoords='offset points')

    ax.set_xlabel('Empleo (L)')
    ax.set_ylabel('Ingresos (R)')
    ax.set_title('Decisión óptima de empleo de la empresa')
    ax.legend()
    ax.grid(True)

    plt.savefig(filename)
    plt.close(fig)
    print(f"Gráfico guardado como {filename}")


def save_iso_profit_curves(filename='custom_iso_profit_curves.png', num_curves=3, w_max=10, L_max=20):
    L = np.linspace(0.1, L_max, 1000)  # Evitamos L=0 para evitar división por cero

    fig, ax = plt.subplots(figsize=(10, 6))

    # Calculamos los niveles de beneficio para las curvas
    profits = np.linspace(5, 25, num_curves)

    for profit in profits:
        # Calculamos w para cada L que da el nivel de beneficio deseado
        w = (revenue_function(L) - profit) / L
        ax.plot(L, w, label=f'π = {profit:.2f}')

    # Añadimos la función de mejor respuesta L*(w)
    w = np.linspace(0, w_max, 100)
    L_opt = (10 - w) / 1  # Asumiendo R(L) = 10L - 0.5L^2
    ax.plot(L_opt, w, 'r--', label='L*(w)')

    ax.set_xlabel('Empleo (L)')
    ax.set_ylabel('Salario (w)')
    ax.set_title('Curvas de isobeneficio de la empresa')
    ax.legend()
    ax.grid(True)
    ax.set_xlim(0, L_max)
    ax.set_ylim(0, w_max)

    plt.savefig(filename)
    plt.close(fig)
    print(f"Gráfico guardado como {filename}")

def save_inefficient_equilibrium(filename='inefficient_equilibrium.png', w_star=5, w_max=10, L_max=10):
    L = np.linspace(0, L_max, 100)

    fig, ax = plt.subplots(figsize=(10, 6))

    L_star = (10 - w_star) / 1

    # Función de mejor respuesta de la empresa
    w = np.linspace(0, w_max, 100)
    L_opt = (10 - w) / 1
    ax.plot(L_opt, w, label='L*(w)')

    # Curva de beneficio de la empresa
    w_curve = w_star + (L - L_star) ** 2
    ax.plot(L, w_curve, label='Curva de beneficio')

    # Punto de equilibrio
    ax.scatter(L_star, w_star, color='red', s=100, zorder=5)
    ax.annotate(f'(L*(w*), w*)=({L_star:.2f}, {w_star:.2f})',
                (L_star, w_star), xytext=(5, 5), textcoords='offset points')

    # Área sombreada
    idx = (L > L_star) & (w_curve < w_star)
    ax.fill_between(L[idx], w_curve[idx], w_star, alpha=0.3, color='gray')

    ax.set_xlabel('Empleo (L)')
    ax.set_ylabel('Salario (w)')
    ax.set_title('Ineficiencia del equilibrio en la negociación')
    ax.legend()
    ax.grid(True)

    plt.savefig(filename)
    plt.close(fig)
    print(f"Gráfico guardado como {filename}")


# Llamadas a las funciones para guardar los gráficos
save_optimal_employment_graph()
save_iso_profit_curves()
save_inefficient_equilibrium()
