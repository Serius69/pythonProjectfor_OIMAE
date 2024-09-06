import pandas as pd
import matplotlib.pyplot as plt

# Cargar el archivo de Excel o CSV
# Asegúrate de reemplazar 'estado_resultados.xlsx' con el nombre de tu archivo y 'Hoja1' con el nombre de la hoja.
df = pd.read_excel('estado_financiero.xlsx', sheet_name='ESTADO DE RESULTADOS')

# Extraer los datos
periodos = df.columns[1:]  # Asume que la primera columna es 'Periodo'
ingresos = df.loc[df['Periodo'] == 'Ventas físicas', periodos].values[0] + \
           df.loc[df['Periodo'] == 'Ventas telefónicas', periodos].values[0]
costo_ventas = df.loc[df['Periodo'] == 'Costo de ventas', periodos].values[0]
costo_variable = df.loc[df['Periodo'] == 'Costo variable', periodos].values[0]
utilidad_bruta = df.loc[df['Periodo'] == 'Utilidad Bruta', periodos].values[0]
gastos_operativos = df.loc[df['Periodo'] == 'Gastos operativos', periodos].values[0]
utilidad_neta = df.loc[df['Periodo'] == 'Utilidad neta', periodos].values[0]

# Calcular márgenes
margen_bruto = (utilidad_bruta / ingresos) * 100
margen_neto = (utilidad_neta / ingresos) * 100

# Cargar el archivo de activos y capital contable para calcular ROA y ROE
# Asume que los datos de activos y capital están en otro archivo o en otra hoja
# df_activos = pd.read_excel('activos_y_capital.xlsx', sheet_name='Hoja1')
# activos_totales = df_activos.loc[df_activos['Periodo'] == 'Total Activos', periodos].values[0]
# capital_contable = df_activos.loc[df_activos['Periodo'] == 'Capital Contable', periodos].values[0]

# Ejemplo con valores ficticios
activos_totales = [100000, 110000, 120000]  # Reemplaza con los datos reales
capital_contable = [50000, 55000, 60000]    # Reemplaza con los datos reales

# Calcular ratios ROA y ROE
ROA = (utilidad_neta / activos_totales) * 100
ROE = (utilidad_neta / capital_contable) * 100

# Graficar los resultados
plt.figure(figsize=(12, 8))

# Ingresos
plt.subplot(2, 3, 1)
plt.plot(periodos, ingresos, marker='o', color='b')
plt.title('Ingresos')
plt.xlabel('Período')
plt.ylabel('Ingresos')
plt.grid(True)

# Costos
plt.subplot(2, 3, 2)
plt.plot(periodos, costo_ventas, marker='o', color='r', label='Costo de Ventas')
plt.plot(periodos, costo_variable, marker='o', color='orange', label='Costo Variable')
plt.title('Costos')
plt.xlabel('Período')
plt.ylabel('Costos')
plt.legend()
plt.grid(True)

# Márgenes
plt.subplot(2, 3, 3)
plt.plot(periodos, [margen_bruto] * len(periodos), marker='o', color='g', label='Margen Bruto')
plt.plot(periodos, [margen_neto] * len(periodos), marker='o', color='m', label='Margen Neto')
plt.title('Márgenes')
plt.xlabel('Período')
plt.ylabel('Margen (%)')
plt.legend()
plt.grid(True)

# Gastos Operativos
plt.subplot(2, 3, 4)
plt.plot(periodos, df.loc[df['Periodo'] == 'Alquiler de oficinas y/o locales', periodos].values[0], marker='o', color='purple', label='Alquiler de Oficinas')
plt.plot(periodos, df.loc[df['Periodo'] == 'Servicios básicos', periodos].values[0], marker='o', color='brown', label='Servicios Básicos')
plt.plot(periodos, df.loc[df['Periodo'] == 'Premios otorgados', periodos].values[0], marker='o', color='cyan', label='Premios Otorgados')
plt.plot(periodos, df.loc[df['Periodo'] == 'Comisiones a vendedores', periodos].values[0], marker='o', color='pink', label='Comisiones a Vendedores')
plt.plot(periodos, df.loc[df['Periodo'] == 'Depreciación', periodos].values[0], marker='o', color='yellow', label='Depreciación')
plt.title('Gastos Operativos')
plt.xlabel('Período')
plt.ylabel('Gastos')
plt.legend()
plt.grid(True)

# Rentabilidad
plt.subplot(2, 3, 5)
plt.plot(periodos, ROA, marker='o', color='blue', label='ROA')
plt.plot(periodos, ROE, marker='o', color='red', label='ROE')
plt.title('Rentabilidad')
plt.xlabel('Período')
plt.ylabel('Rentabilidad (%)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
