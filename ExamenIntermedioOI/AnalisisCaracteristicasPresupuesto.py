import matplotlib.pyplot as plt
import numpy as np

# Datos para las 7 P's del marketing
categories = ['Producto', 'Precio', 'Plaza', 'Promoción', 'Personas', 'Procesos', 'Evidencia Física']
base_budget = [20, 15, 10, 25, 10, 10, 10]
moderate_change = [5, 10, 5, 15, 5, 5, 5]
significant_change = [10, 20, 15, 30, 10, 15, 10]

# Crear el gráfico
fig, ax = plt.subplots(figsize=(12, 8))

# Posiciones de las barras
y_pos = np.arange(len(categories))

# Crear barras apiladas
ax.barh(y_pos, base_budget, align='center', alpha=0.8, label='Presupuesto Base')
ax.barh(y_pos, moderate_change, left=base_budget, align='center', alpha=0.8, label='Cambio Moderado')
ax.barh(y_pos, significant_change, left=np.array(base_budget) + np.array(moderate_change), align='center', alpha=0.8, label='Cambio Significativo')

# Personalizar el gráfico
ax.set_yticks(y_pos)
ax.set_yticklabels(categories)
ax.invert_yaxis()  # Invertir el eje Y para que la primera categoría esté arriba
ax.set_xlabel('Presupuesto (%)')
ax.set_title('Análisis de Sensibilidad - Producción de Boletos de Lotería')

# Añadir una leyenda
ax.legend()

# Añadir etiquetas de valor en las barras
for i, category in enumerate(categories):
    total = base_budget[i] + moderate_change[i] + significant_change[i]
    ax.text(total + 1, i, f'{total}%', va='center')

# Ajustar el diseño y mostrar el gráfico
plt.tight_layout()
plt.show()