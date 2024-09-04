import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configurar estilo de los gráficos
sns.set(style="whitegrid")

# Función para limpiar y convertir los datos
def clean_value(x):
    if isinstance(x, str):
        x = x.replace('%', '').replace(',', '.').strip()
        if x == '':
            return np.nan
        try:
            return float(x)
        except ValueError:
            return x  # Retorna el valor original si no se puede convertir
    return x

# Cargar el archivo CSV
try:
    df = pd.read_csv('archivo.csv', header=None, skip_blank_lines=False)
except FileNotFoundError:
    raise FileNotFoundError("El archivo 'archivo.csv' no se encontró en la ruta especificada.")

# Identificar los índices donde comienzan las secciones
wacc_start = df[df[0].str.strip() == 'WACC'].index
flujo_start = df[df[0].str.strip() == 'FLUJO DE CAJA LIBRE'].index

if wacc_start.empty or flujo_start.empty:
    raise ValueError("No se encontraron las secciones 'Estimación WACC' o 'FLUJO DE CAJA LIBRE' en el CSV.")

wacc_start = wacc_start[0]
flujo_start = flujo_start[0]

# Extraer las secciones de Estimación WACC y Flujo de Caja Libre
df_wacc = df.iloc[wacc_start + 1:flujo_start].copy()
df_flujo = df.iloc[flujo_start + 1:].copy()

# Renombrar las columnas utilizando la primera fila de cada sección
df_wacc.columns = df_wacc.iloc[0].str.strip()
df_wacc = df_wacc[1:].reset_index(drop=True)

df_flujo.columns = df_flujo.iloc[0].str.strip()
df_flujo = df_flujo[1:].reset_index(drop=True)

# Aplicar la función de limpieza a todas las celdas
df_wacc = df_wacc.applymap(clean_value)
df_flujo = df_flujo.applymap(clean_value)

# Transponer los DataFrames para facilitar el acceso
df_wacc_t = df_wacc.transpose()
df_flujo_t = df_flujo.transpose()

# Convertir los índices a números (escenarios)
df_wacc_t.index = df_wacc_t.index.astype(int)
df_flujo_t.index = df_flujo_t.index.astype(int)

# Extraer variables clave de la sección Estimación WACC
try:
    rf = df_wacc_t['rf'][0]  # Tasa libre de riesgo
    beta_empresa = df_wacc_t['Beta empresa'][0]  # Beta de la empresa
    erm = df_wacc_t['E(rm)'][0]  # Rendimiento del mercado
    prima_riesgo_pais = df_wacc_t['Prima de riesgo pais'][0]  # Prima de riesgo país
except KeyError as e:
    raise KeyError(f"Falta la columna necesaria en 'Estimación WACC': {e}")

# Calcular el WACC original si es necesario
# Aquí asumimos que WACC = rf + Beta * (E(rm) + Prima de riesgo pais)
# Ajusta esta fórmula según la estructura real de tu WACC
wacc_original = rf + beta_empresa * (erm + prima_riesgo_pais)

# Extraer variables clave de la sección Flujo de Caja Libre
try:
    fcff = df_flujo_t['FCFF'].astype(float).values  # Flujo de Caja Libre
except KeyError:
    raise KeyError("Falta la columna 'FCFF' en 'FLUJO DE CAJA LIBRE'.")

# Extraer VAN y TIR originales
try:
    van_original = df_flujo_t.loc['VAN'][0]
    tir_original = df_flujo_t.loc['TIR'][0]
except KeyError:
    van_original = np.nan
    tir_original = np.nan

# Definir funciones para calcular VAN y TIR
def calcular_van(wacc, flujo):
    """Calcula el Valor Actual Neto (VAN) dado un WACC y los flujos de caja."""
    van = np.sum(flujo / (1 + wacc) ** np.arange(1, len(flujo) + 1))
    return van

def calcular_tir(flujo):
    """Calcula la Tasa Interna de Retorno (TIR) dado los flujos de caja."""
    tir = np.irr(flujo)
    return tir

# Análisis de Sensibilidad: Variar WACC
wacc_variations = np.arange(0.05, 0.25, 0.01)  # De 5% a 24% en incrementos de 1%

vans = []
tirs = []

for wacc_val in wacc_variations:
    van = calcular_van(wacc_val, fcff)
    tir = calcular_tir(fcff)  # TIR no depende de WACC, se puede calcular una vez
    vans.append(van)
    tirs.append(tir)

# Crear un DataFrame para almacenar los resultados
sensitivity_df = pd.DataFrame({
    'WACC': wacc_variations,
    'VAN': vans,
    'TIR': tirs
})

# Calcular TIR una vez ya que no depende de WACC
sensitivity_df['TIR'] = tirs  # Todas las filas tendrán el mismo valor

# Visualización del Análisis de Sensibilidad

# Gráfico de VAN vs WACC
plt.figure(figsize=(12, 8))
sns.lineplot(x='WACC', y='VAN', data=sensitivity_df, marker='o', label='VAN')
plt.axhline(0, color='red', linestyle='--', label='VAN = 0')
plt.title('Análisis de Sensibilidad: VAN vs WACC', fontsize=16)
plt.xlabel('WACC', fontsize=14)
plt.ylabel('VAN', fontsize=14)
plt.legend()
plt.grid(True)
plt.show()

# Gráfico de TIR vs WACC
plt.figure(figsize=(12, 8))
sns.lineplot(x='WACC', y='TIR', data=sensitivity_df, marker='o', label='TIR')
plt.axhline(tir_original, color='green', linestyle='--', label=f'TIR Original = {tir_original:.2%}')
plt.title('Análisis de Sensibilidad: TIR vs WACC', fontsize=16)
plt.xlabel('WACC', fontsize=14)
plt.ylabel('TIR', fontsize=14)
plt.legend()
plt.grid(True)
plt.show()

# Guardar los resultados del análisis en un archivo CSV
sensitivity_df.to_csv('resultados_sensibilidad.csv', index=False)

print("Análisis de sensibilidad completado y resultados guardados en 'resultados_sensibilidad.csv'.")