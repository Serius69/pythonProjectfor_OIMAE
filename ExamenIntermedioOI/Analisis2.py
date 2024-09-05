import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Definir los datos
data = [
    [-375, -325, -275, -225, -175, -125],
    [-325, -255, -185, -115, -45, 25],
    [-275, -185, -95, -5, 85, 175],
    [-225, -115, -5, 105, 215, 325],
    [-175, -45, 85, 215, 345, 475],
    [-125, 25, 175, 325, 475, 625]
]

# Crear el DataFrame
df = pd.DataFrame(data, index=['-20%', '-15%', '-10%', '-5%', '0%', '5%','10%','15%','20%'],
                  columns=[2500, 3500, 4500, 5500, 6500, 7500])

# Graficar los datos
plt.figure(figsize=(12, 8))
sns.heatmap(df, annot=True, cmap="RdYlGn")
plt.title("Análisis de Sensibilidad - Precio de Diamantes")
plt.xlabel("Promedio de precio de diamantes [$USD]")
plt.ylabel("Monto vendido [$ mil]")
plt.show()

# Análisis de sensibilidad
sensitivity = df.to_numpy()
profit_changes = []

for i in range(len(df.index)):
    for j in range(len(df.columns)):
        # Calcular el cambio de ganancia para cada combinación de monto vendido y precio
        profit_change = (sensitivity[i, j] - sensitivity[i-1, j-1]) / sensitivity[i-1, j-1] * 100
        profit_changes.append(profit_change)

# Crear un DataFrame con los cambios de ganancia
sensitivity_df = pd.DataFrame({
    "Monto vendido [$ mil]": np.repeat(df.index, len(df.columns)),
    "Promedio de precio de diamantes [$USD]": np.tile(df.columns, len(df.index)),
    "Cambio de ganancia (%)": profit_changes
})

# Mostrar el análisis de sensibilidad
print(sensitivity_df)