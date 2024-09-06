import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Leer el archivo Excel
df = pd.read_excel('estado_financiero.xlsx', sheet_name='BALANCE GENERAL')

# Extraer los valores necesarios
activo_corriente = df.loc[df['ACTIVOS'] == 'TOTAL ACTIVO CORRIENTE', ['2024', '2025', '2026']].values[0]
activo_no_corriente = df.loc[df['ACTIVOS'] == 'TOTAL ACTIVO NO CORRIENTE', ['2024', '2025', '2026']].values[0]
pasivo_corriente = df.loc[df['PASIVO Y PATRIMONIO NETO'] == 'TOTAL PASIVO CORRIENTE', ['2024', '2025', '2026']].values[0]
pasivo_no_corriente = df.loc[df['PASIVO Y PATRIMONIO NETO'] == 'TOTAL PASIVO NO CORRIENTE', ['2024', '2025', '2026']].values[0]
patrimonio_neto = df.loc[df['PASIVO Y PATRIMONIO NETO'] == 'TOTAL PATRIMONIO NETO', ['2024', '2025', '2026']].values[0]

# Calcular los ratios financieros base
deuda_total = pasivo_corriente + pasivo_no_corriente
activo_total = activo_corriente + activo_no_corriente

ratio_deuda = deuda_total / activo_total
ratio_corriente = activo_corriente / pasivo_corriente
capital_trabajo = activo_corriente - pasivo_corriente
relacion_activos_fondos_propios = activo_total / patrimonio_neto
relacion_deuda_fondos_propios = deuda_total / patrimonio_neto

# Crear un DataFrame para los ratios base
ratios_base = pd.DataFrame({
    'Ratios Financieros': ['Ratio de Deuda', 'Ratio Corriente', 'Capital de Trabajo', 'Relación Activos/Fondos Propios', 'Relación Deuda/Fondos Propios'],
    '2024': [ratio_deuda[0], ratio_corriente[0], capital_trabajo[0], relacion_activos_fondos_propios[0], relacion_deuda_fondos_propios[0]],
    '2025': [ratio_deuda[1], ratio_corriente[1], capital_trabajo[1], relacion_activos_fondos_propios[1], relacion_deuda_fondos_propios[1]],
    '2026': [ratio_deuda[2], ratio_corriente[2], capital_trabajo[2], relacion_activos_fondos_propios[2], relacion_deuda_fondos_propios[2]]
})

# Guardar los ratios base en un archivo Excel
ratios_base.to_excel('ratios_base.xlsx', index=False)

# Definir los escenarios (por ejemplo, cambios porcentuales en los valores)
escenarios = {
    'Escenario 1': [0.95, 0.97, 1.00],  # Disminución del 5% en 2024, 3% en 2025, sin cambio en 2026
    'Escenario 2': [1.05, 1.03, 1.00],  # Aumento del 5% en 2024, 3% en 2025, sin cambio en 2026
    'Escenario 3': [1.10, 1.10, 1.10],  # Aumento del 10% en todos los años
    'Escenario 4': [0.90, 0.90, 0.90],  # Disminución del 10% en todos los años
    'Escenario 5': [1.00, 0.95, 0.90],  # Sin cambio en 2024, disminución del 5% en 2025, 10% en 2026
    'Escenario 6': [0.80, 0.85, 0.90],  # Disminución del 20% en 2024, 15% en 2025, 10% en 2026
}

# Simulación de escenarios
resultados = {}
for escenario, ajustes in escenarios.items():
    deuda_total_ajustada = deuda_total * np.array(ajustes)
    activo_total_ajustado = activo_total * np.array(ajustes)
    patrimonio_neto_ajustado = patrimonio_neto * np.array(ajustes)

    ratio_deuda = deuda_total_ajustada / activo_total_ajustado
    ratio_corriente = (activo_corriente * np.array(ajustes)) / (pasivo_corriente * np.array(ajustes))
    capital_trabajo = (activo_corriente * np.array(ajustes)) - (pasivo_corriente * np.array(ajustes))
    relacion_activos_fondos_propios = activo_total_ajustado / patrimonio_neto_ajustado
    relacion_deuda_fondos_propios = deuda_total_ajustada / patrimonio_neto_ajustado

    resultados[escenario] = {
        'Ratio Deuda': ratio_deuda,
        'Ratio Corriente': ratio_corriente,
        'Capital de Trabajo': capital_trabajo,
        'Relación Activos/Fondos Propios': relacion_activos_fondos_propios,
        'Relación Deuda/Fondos Propios': relacion_deuda_fondos_propios
    }

# Guardar las simulaciones en un archivo Excel
simulaciones_df = pd.DataFrame(columns=['Escenario', 'Año', 'Ratio Deuda', 'Ratio Corriente', 'Capital de Trabajo', 'Relación Activos/Fondos Propios', 'Relación Deuda/Fondos Propios'])
for escenario in resultados:
    for i, year in enumerate(['2024', '2025', '2026']):
        simulaciones_df = simulaciones_df.append({
            'Escenario': escenario,
            'Año': year,
            'Ratio Deuda': resultados[escenario]['Ratio Deuda'][i],
            'Ratio Corriente': resultados[escenario]['Ratio Corriente'][i],
            'Capital de Trabajo': resultados[escenario]['Capital de Trabajo'][i],
            'Relación Activos/Fondos Propios': resultados[escenario]['Relación Activos/Fondos Propios'][i],
            'Relación Deuda/Fondos Propios': resultados[escenario]['Relación Deuda/Fondos Propios'][i]
        }, ignore_index=True)
simulaciones_df.to_excel('simulaciones_scenarios.xlsx', index=False)

# Graficar los resultados
sns.set(style="whitegrid")
years = ['2024', '2025', '2026']

for ratio_name in ['Ratio Deuda', 'Ratio Corriente', 'Capital de Trabajo', 'Relación Activos/Fondos Propios', 'Relación Deuda/Fondos Propios']:
    plt.figure(figsize=(10, 6))
    for escenario in escenarios.keys():
        plt.plot(years, resultados[escenario][ratio_name], marker='o', label=escenario)
    plt.title(ratio_name)
    plt.xlabel('Año')
    plt.ylabel(ratio_name)
    plt.legend()
    plt.show()

print("Análisis de sensibilidad y simulaciones completadas. Resultados guardados en 'ratios_base.xlsx' y 'simulaciones_scenarios.xlsx'.")
