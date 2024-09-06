import pandas as pd
import matplotlib.pyplot as plt

# Cargar el archivo de Excel o CSV
# Asegúrate de reemplazar 'flujo_caja.xlsx' con el nombre de tu archivo y 'Hoja1' con el nombre de la hoja.
df = pd.read_excel('estado_financiero.xlsx', sheet_name='FLUJO DE CAJA')

# Extraer los datos
periodos = df.columns[1:]  # Asume que la primera columna es 'Periodo'
EBIT = df.loc[df['FLUJO DE CAJA LIBRE'] == 'EBIT (1-tx)', periodos].values[0]
depreciacion = df.loc[df['FLUJO DE CAJA LIBRE'] == '(+) Depreciación', periodos].values[0]
var_capex = df.loc[df['FLUJO DE CAJA LIBRE'] == '(-) Var Capex', periodos].values[0]
working_capital = df.loc[df['FLUJO DE CAJA LIBRE'] == '(-)Working Capital', periodos].values[0]
inversiones = df.loc[df['FLUJO DE CAJA LIBRE'] == 'Inversiones', periodos].values[0]
FCFF = df.loc[df['FLUJO DE CAJA LIBRE'] == 'FCFF', periodos].values[0]
flujo_desc = df.loc[df['FLUJO DE CAJA LIBRE'] == 'Flujo Descontados', periodos].values[0]
VAN = df.loc[df['FLUJO DE CAJA LIBRE'] == 'VAN', periodos].values[0]
TIR = df.loc[df['FLUJO DE CAJA LIBRE'] == 'TIR', periodos].values[0]

# Calcular flujo de caja operativo
flujo_caja_operativo = EBIT + depreciacion - var_capex - working_capital

# Calcular flujo de caja neto
flujo_caja_neto = flujo_caja_operativo - inversiones

# Graficar los resultados
plt.figure(figsize=(14, 10))

# Ingresos Operativos
plt.subplot(2, 3, 1)
plt.plot(periodos, EBIT, marker='o', color='b', label='EBIT (1-tx)')
plt.title('Ingresos Operativos')
plt.xlabel('Período')
plt.ylabel('EBIT (1-tx)')
plt.grid(True)
plt.legend()

# Salidas de Efectivo
plt.subplot(2, 3, 2)
plt.plot(periodos, var_capex, marker='o', color='r', label='Var Capex')
plt.plot(periodos, working_capital, marker='o', color='orange', label='Working Capital')
plt.plot(periodos, inversiones, marker='o', color='purple', label='Inversiones')
plt.title('Salidas de Efectivo')
plt.xlabel('Período')
plt.ylabel('Salidas de Efectivo')
plt.legend()
plt.grid(True)

# Flujo de Caja Operativo
plt.subplot(2, 3, 3)
plt.plot(periodos, flujo_caja_operativo, marker='o', color='g', label='Flujo de Caja Operativo')
plt.title('Flujo de Caja Operativo')
plt.xlabel('Período')
plt.ylabel('Flujo de Caja Operativo')
plt.grid(True)
plt.legend()

# Flujo de Caja Neto
plt.subplot(2, 3, 4)
plt.plot(periodos, flujo_caja_neto, marker='o', color='m', label='Flujo de Caja Neto')
plt.title('Flujo de Caja Neto')
plt.xlabel('Período')
plt.ylabel('Flujo de Caja Neto')
plt.grid(True)
plt.legend()

# Flujo Descontado
plt.subplot(2, 3, 5)
plt.plot(periodos, flujo_desc, marker='o', color='c', label='Flujo Descontado')
plt.title('Flujo Descontado')
plt.xlabel('Período')
plt.ylabel('Flujo Descontado')
plt.grid(True)
plt.legend()

# VAN y TIR
plt.subplot(2, 3, 6)
plt.plot(periodos, VAN, marker='o', color='y', label='VAN')
plt.plot(periodos, TIR, marker='o', color='b', label='TIR')
plt.title('VAN y TIR')
plt.xlabel('Período')
plt.ylabel('VAN / TIR')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()

# Conclusiones
print("Conclusiones:")
print(f"Flujo de Caja Operativo: {flujo_caja_operativo}")
print(f"Flujo de Caja Neto: {flujo_caja_neto}")
print(f"Flujo Descontado: {flujo_desc}")
print(f"VAN: {VAN}")
print(f"TIR: {TIR}")
