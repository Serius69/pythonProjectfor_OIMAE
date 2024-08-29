import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, widgets

def revenue_function(L):
    return 3850 * L - 5 * L**2

def create_figure(figsize=(12, 8)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlabel('Empleo (L)', fontsize=12)
    ax.set_ylabel('Salario (w)', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.tick_params(axis='both', which='major', labelsize=10)
    return fig, ax

def save_figure(fig, filename, title):
    plt.title(title, fontsize=16)
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Gráfico guardado como {filename}")

def plot_curve(ax, x, y, label, color, linestyle='-'):
    return ax.plot(x, y, label=label, color=color, linestyle=linestyle)

def plot_point(ax, x, y, color, label):
    ax.scatter(x, y, color=color, s=100, zorder=5)
    ax.annotate(f'{label}: ({x:.2f}, {y:.2f})', (x, y),
                xytext=(5, 5), textcoords='offset points', color=color)

def plot_optimal_employment(w_max=10, L_max=10):
    L = np.linspace(0, L_max, 100)
    R = revenue_function(L)

    fig, ax = create_figure((10, 6))

    def update(w):
        ax.clear()
        plot_curve(ax, L, R, 'R(L)', 'blue')
        plot_curve(ax, L, w * L, f'wL (w={w:.2f})', 'orange')

        L_opt = (10 - w) / 1
        R_opt = revenue_function(L_opt)
        plot_point(ax, L_opt, R_opt, 'red', f'L*(w)={L_opt:.2f}')

        ax.set_xlabel('Empleo (L)')
        ax.set_ylabel('Ingresos (R)')
        ax.legend()
        ax.grid(True)

    interact(update, w=widgets.FloatSlider(min=0, max=w_max, step=0.1, value=5))

def plot_iso_profit_curves(w_max=3000, L_max=300):
    L = np.linspace(0, L_max, 100)

    fig, ax = create_figure((10, 6))

    def update(num_curves):
        ax.clear()
        for i in range(num_curves):
            w = np.linspace(0, w_max, 100)
            L_opt = (3850 - w) / 5
            plot_curve(ax, L_opt, w, f'Curva {i + 1}', plt.cm.viridis(i / num_curves))

        ax.set_xlabel('Empleo (L)')
        ax.set_ylabel('Salario (w)')
        ax.legend()
        ax.grid(True)

    interact(update, num_curves=widgets.IntSlider(min=1, max=5, step=1, value=3))

def plot_inefficient_equilibrium(w_max=3000, L_max=270):
    L = np.linspace(0, L_max, 100)

    fig, ax = create_figure((10, 6))

    def update(w_star):
        ax.clear()
        L_star = (3850 - w_star) / 5

        w = np.linspace(0, w_max, 100)
        L_opt = (3850 - w) / 5
        plot_curve(ax, L_opt, w, 'L*(w)', 'red', '--')

        w_curve = w_star + (L - L_star) ** 2
        plot_curve(ax, L, w_curve, 'Curva de beneficio', 'blue')

        plot_point(ax, L_star, w_star, 'red', '(L*(w*), w*)')

        idx = (L > L_star) & (w_curve < w_star)
        ax.fill_between(L[idx], w_curve[idx], w_star, alpha=0.3, color='gray')

        ax.set_xlabel('Empleados (L)')
        ax.set_ylabel('Salario (w)')
        ax.legend()
        ax.grid(True)

    interact(update, w_star=widgets.FloatSlider(min=0, max=w_max, step=0.1, value=5))

def save_optimal_employment_graph(filename='optimal_employment_area.png', w_values=[2500, 3000], w_max=3000, L_max=270):
    L = np.linspace(0, L_max, 100)
    fig, ax = create_figure((10, 6))

    R = revenue_function(L)
    plot_curve(ax, L, R, 'R(L)', 'black')

    for w in w_values:
        plot_curve(ax, L, w * L, f'wL (w={w})', 'gray', '--')
        L_opt = (3850 - w) / 5
        R_opt = revenue_function(L_opt)
        plot_point(ax, L_opt, R_opt, 'red', f'L*(w={w})')

    L_inter = np.linspace((3850 - w_values[1]) / 5, (3850 - w_values[0]) / 5, 100)
    ax.fill_between(L_inter, w_values[0] * L_inter, w_values[1] * L_inter, color='gray', alpha=0.5)

    ax.invert_xaxis()
    ax.invert_yaxis()
    ax.set_xlabel('L')
    ax.set_ylabel('w')
    ax.legend().set_visible(False)

    save_figure(fig, filename, 'Curva de beneficio de la empresa')

def save_iso_profit_curves(filename='iso_profit_curves.png', num_curves=5, w_max=3000, L_max=300):
    L = np.linspace(1, L_max, 1000)
    fig, ax = create_figure((12, 8))

    profits = np.linspace(150000, 250000, num_curves)
    for profit in profits:
        w = np.clip((revenue_function(L) - profit) / L, 0, w_max)
        plot_curve(ax, L, w, f'π = {profit:,.0f}', plt.cm.viridis(profit / profits[-1]))

    # Asegurando intersección correcta entre L*(w) y las curvas de isobeneficio
    w_values = np.linspace(0, w_max, 100)
    L_opt = np.clip((3850 - w_values) / 5, 0, L_max)
    plot_curve(ax, L_opt, w_values, 'L*(w)', 'red', '--')

    ax.set_xlim(0, L_max)
    ax.set_ylim(0, w_max)
    fig.text(0.95, 0.05, 'Creado con Python', fontsize=8, color='gray', ha='right', va='bottom', alpha=0.5)

    save_figure(fig, filename, 'Curvas de isobeneficio de la empresa')

def save_inefficient_equilibrium(filename='inefficient_equilibrium.png', w_star=2500, w_max=3000, L_max=300):
    L = np.linspace(100, L_max, 1000)
    fig, ax = create_figure((10, 6))

    L_star = (3850 - w_star) / 5

    w = np.linspace(0, w_max, 100)
    L_opt = (3850 - w) / 5
    plot_curve(ax, L_opt, w, 'L*(w)', 'red', '--')

    profit_level = revenue_function(L_star) - w_star * L_star
    w_curve = np.clip((revenue_function(L) - profit_level) / L, 0, w_max)
    plot_curve(ax, L, w_curve, 'Curva de beneficio', 'blue')

    plot_point(ax, L_star, w_star, 'red', '(L*(w*), w*)')

    idx = (L > L_star) & (w_curve < w_star)
    ax.fill_between(L[idx], w_curve[idx], w_star, alpha=0.3, color='gray')

    ax.set_xlim(0, L_max)
    ax.set_ylim(0, w_max)

    save_figure(fig, filename, 'Ineficiencia del equilibrio en la negociación')

# Ejecutar las funciones para guardar los gráficos
save_optimal_employment_graph()
save_iso_profit_curves()
save_inefficient_equilibrium()
