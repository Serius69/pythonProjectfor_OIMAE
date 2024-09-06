import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Leer los datos desde un archivo Excel
df = pd.read_excel('data_prueba_sensibilidad.xlsx', index_col=0)

# Graficar el heatmap de sensibilidad (VAN)
plt.figure(figsize=(12, 8))
sns.heatmap(df, annot=True, cmap="RdYlGn", cbar_kws={'label': 'Diferencia respecto al VAN (Valos Absoluto Neto)'})
plt.title("Análisis de Sensibilidad - Precio de boletos de Lotería vs Monto Vendido")
plt.xlabel("Precio boleto [Bs]")
plt.ylabel("Cantidad de Boletos vendido [uni]")
plt.show()

# Análisis de sensibilidad: calcular cambios porcentuales del VAN
sensitivity = df.to_numpy()
profit_changes = []

# Recorrer todas las celdas excepto la primera fila y columna para evitar errores de índice
for i in range(1, len(df.index)):  # Empieza desde la segunda fila
    for j in range(1, len(df.columns)):  # Empieza desde la segunda columna
        # Calcular el cambio porcentual respecto al valor anterior (fila anterior y columna anterior)
        profit_change = (sensitivity[i, j] - sensitivity[i-1, j-1]) / abs(sensitivity[i-1, j-1]) * 100
        profit_changes.append(profit_change)

# Crear un DataFrame con los cambios de ganancia
sensitivity_df = pd.DataFrame({
    "Monto vendido [$ mil]": np.repeat(df.index[1:], len(df.columns) - 1),  # Excluir primera fila
    "Precio boleto [Bs]": np.tile(df.columns[1:], len(df.index) - 1),  # Excluir primera columna
    "Cambio de ganancia (%)": profit_changes
})

# Mostrar el análisis de sensibilidad (cambios porcentuales)
print(sensitivity_df)
