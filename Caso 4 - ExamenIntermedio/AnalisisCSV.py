# df = pd.read_excel('prueba.xlsx', sheet_name='Hoja1')

import pandas as pd
import matplotlib.pyplot as plt

# Cargar el archivo de Excel o CSV
df = pd.read_excel('prueba.xlsx', sheet_name='Hoja1')

# Verifica los nombres de las columnas y los valores disponibles
print("Columnas disponibles:", df.columns)
print("Primeras filas del DataFrame:")
print(df.head())

# Asegúrate de que el nombre de la columna sea correcto
columna_estado = 'ESTADO DE RESULTADOS'

# Verifica los valores únicos en la columna para asegurarte de que estás buscando correctamente
print("Valores únicos en la columna 'ESTADO DE RESULTADOS':", df[columna_estado].unique())

# Extraer los datos
ventas = df.loc[df[columna_estado] == 'Ventas', df.columns[1:]].values
if ventas.size == 0:
    raise ValueError("No se encontraron datos para 'Ventas'")
ventas = ventas[0]

costo_venta = df.loc[df[columna_estado] == 'Costo de venta', df.columns[1:]].values
if costo_venta.size == 0:
    raise ValueError("No se encontraron datos para 'Costo de venta'")
costo_venta = costo_venta[0]

utilidad_bruta = df.loc[df[columna_estado] == 'Utilidad Bruta', df.columns[1:]].values
if utilidad_bruta.size == 0:
    raise ValueError("No se encontraron datos para 'Utilidad Bruta'")
utilidad_bruta = utilidad_bruta[0]

gastos_admin = df.loc[df[columna_estado] == 'Gastos admin', df.columns[1:]].values
if gastos_admin.size == 0:
    raise ValueError("No se encontraron datos para 'Gastos admin'")
gastos_admin = gastos_admin[0]

utilidad_neta = df.loc[df[columna_estado] == 'Utilidad neta', df.columns[1:]].values
if utilidad_neta.size == 0:
    raise ValueError("No se encontraron datos para 'Utilidad neta'")
utilidad_neta = utilidad_neta[0]

# Ejemplo con valores ficticios
activos_totales = [100000, 110000, 120000, 130000, 140000]  # Reemplaza con los datos reales
capital_contable = [50000, 55000, 60000, 65000, 70000]    # Reemplaza con los datos reales

# Calcular márgenes
margen_bruto = (utilidad_bruta / ventas) * 100
margen_neto = (utilidad_neta / ventas) * 100

# Calcular ratios ROA y ROE
ROA = (utilidad_neta / activos_totales) * 100
ROE = (utilidad_neta / capital_contable) * 100

# Graficar los resultados
plt.figure(figsize=(14, 10))

# Ingresos
plt.subplot(2, 3, 1)
plt.plot(df.columns[1:], ventas, marker='o', color='b')
plt.title('Ventas')
plt.xlabel('Período')
plt.ylabel('Ventas')
plt.grid(True)

# Costos
plt.subplot(2, 3, 2)
plt.plot(df.columns[1:], costo_venta, marker='o', color='r', label='Costo de Ventas')
plt.title('Costos')
plt.xlabel('Período')
plt.ylabel('Costos')
plt.legend()
plt.grid(True)

# Márgenes
plt.subplot(2, 3, 3)
plt.plot(df.columns[1:], [margen_bruto.mean()] * len(df.columns[1:]), marker='o', color='g', label='Margen Bruto')
plt.plot(df.columns[1:], [margen_neto.mean()] * len(df.columns[1:]), marker='o', color='m', label='Margen Neto')
plt.title('Márgenes')
plt.xlabel('Período')
plt.ylabel('Margen (%)')
plt.legend()
plt.grid(True)

# Gastos Operativos
plt.subplot(2, 3, 4)
plt.plot(df.columns[1:], gastos_admin, marker='o', color='purple', label='Gastos Administrativos')
plt.title('Gastos Operativos')
plt.xlabel('Período')
plt.ylabel('Gastos')
plt.legend()
plt.grid(True)

# Rentabilidad
plt.subplot(2, 3, 5)
plt.plot(df.columns[1:], ROA, marker='o', color='blue', label='ROA')
plt.plot(df.columns[1:], ROE, marker='o', color='red', label='ROE')
plt.title('Rentabilidad')
plt.xlabel('Período')
plt.ylabel('Rentabilidad (%)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

