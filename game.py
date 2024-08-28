import numpy as np
import matplotlib.pyplot as plt

# Definir las estrategias
strategies_empresa = ['Salario Bajo', 'Salario Alto']
strategies_trabajadores = ['Aceptar', 'Rechazar']

# Definir la matriz de pagos
# Formato: (pago_empresa, pago_trabajadores)
payoff_matrix = np.array([[(4, 2), (0, 0)],
                          [(3, 3), (1, 2)]])

# Graficar los pagos
fig, ax = plt.subplots()
ax.set_xticks(np.arange(len(strategies_empresa)))
ax.set_yticks(np.arange(len(strategies_trabajadores)))

# Etiquetas de las estrategias
ax.set_xticklabels(strategies_empresa)
ax.set_yticklabels(strategies_trabajadores)

# Mostrar los pagos en cada celda de la matriz
for i in range(len(strategies_empresa)):
    for j in range(len(strategies_trabajadores)):
        payoff = payoff_matrix[i, j]
        ax.text(j, i, f"{payoff[0]}, {payoff[1]}", ha='center', va='center', color='black')

# Ajustes de la gráfica
ax.set_title('Matriz de Pagos: Empresa vs Trabajadores')
ax.set_xlabel('Trabajadores')
ax.set_ylabel('Empresa')
plt.show()
