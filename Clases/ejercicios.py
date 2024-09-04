import numpy as np
import matplotlib.pyplot as plt

# Datos del problema
p = 0.30  # Probabilidad de lluvia excepcional
YLL_trigo, YLN_trigo = 10000, 28000  # Rendimientos del trigo
YLL_maiz, YLN_maiz = 15000, 19000  # Rendimientos del maíz

# Función de utilidad esperada
def utilidad_esperada(YLL, YLN):
    return (1/3) * p * YLL + (2/3) * (1-p) * YLN

# a) Análisis de cultivos individuales
util_trigo = utilidad_esperada(YLL_trigo, YLN_trigo)
util_maiz = utilidad_esperada(YLL_maiz, YLN_maiz)

print(f"a) Utilidad esperada del trigo: {util_trigo:.2f}")
print(f"   Utilidad esperada del maíz: {util_maiz:.2f}")
print(f"   Se debe sembrar: {'Trigo' if util_trigo > util_maiz else 'Maíz'}")

# b) Análisis de cultivo mixto
proporciones = np.linspace(0, 1, 100)
utilidades = []

for prop_trigo in proporciones:
    prop_maiz = 1 - prop_trigo
    util = utilidad_esperada(prop_trigo*YLL_trigo + prop_maiz*YLL_maiz,
                             prop_trigo*YLN_trigo + prop_maiz*YLN_maiz)
    utilidades.append(util)

indice_optimo = np.argmax(utilidades)
prop_optima = proporciones[indice_optimo]
util_optima = utilidades[indice_optimo]

print(f"\nb) Proporción óptima: {prop_optima:.2%} de trigo y {1-prop_optima:.2%} de maíz")
print(f"   Utilidad esperada máxima: {util_optima:.2f}")

# c) Comparación de estrategias
util_mitad = utilidad_esperada(0.5*YLL_trigo + 0.5*YLL_maiz, 0.5*YLN_trigo + 0.5*YLN_maiz)
print(f"\nc) Utilidad esperada (50% cada cultivo): {util_mitad:.2f}")
print(f"   Mejor estrategia: {'Mixta óptima' if util_optima > util_mitad else '50% cada cultivo'}")

# d) Análisis con seguro para el trigo
costo_seguro = 8000
beneficio_seguro = 40000

def utilidad_con_seguro(YLL, YLN):
    return (1/3) * p * (YLL + beneficio_seguro - costo_seguro) + (2/3) * (1-p) * (YLN - costo_seguro)

util_trigo_seguro = utilidad_con_seguro(YLL_trigo, YLN_trigo)
print(f"\nd) Utilidad esperada del trigo con seguro: {util_trigo_seguro:.2f}")
print(f"   Conviene el seguro: {'Sí' if util_trigo_seguro > util_trigo else 'No'}")

# Gráficos
plt.figure(figsize=(15, 10))

# Gráfico 1: Utilidad esperada vs Proporción de cultivos
plt.subplot(2, 2, 1)
plt.plot(proporciones, utilidades, 'b-')
plt.plot(prop_optima, util_optima, 'ro', label='Óptimo')
plt.xlabel('Proporción de Trigo')
plt.ylabel('Utilidad Esperada')
plt.title('Utilidad Esperada vs Proporción de Cultivos')
plt.legend()
plt.grid(True)

# Gráfico 2: Comparación de estrategias
plt.subplot(2, 2, 2)
estrategias = ['Trigo', 'Maíz', 'Mixta Óptima', '50% cada']
utils = [util_trigo, util_maiz, util_optima, util_mitad]
plt.bar(estrategias, utils)
plt.ylabel('Utilidad Esperada')
plt.title('Comparación de Estrategias')

# Gráfico 3: Impacto del seguro en el trigo
plt.subplot(2, 2, 3)
plt.bar(['Sin Seguro', 'Con Seguro'], [util_trigo, util_trigo_seguro])
plt.ylabel('Utilidad Esperada')
plt.title('Impacto del Seguro en el Trigo')

# Gráfico 4: Distribución de utilidades en diferentes escenarios
plt.subplot(2, 2, 4)
escenarios = ['Lluvia (Trigo)', 'Normal (Trigo)', 'Lluvia (Maíz)', 'Normal (Maíz)']
utilidades_escenarios = [YLL_trigo, YLN_trigo, YLL_maiz, YLN_maiz]
plt.bar(escenarios, utilidades_escenarios)
plt.ylabel('Utilidad')
plt.title('Utilidades en Diferentes Escenarios')
plt.xticks(rotation=45, ha='right')

plt.tight_layout()
plt.show()