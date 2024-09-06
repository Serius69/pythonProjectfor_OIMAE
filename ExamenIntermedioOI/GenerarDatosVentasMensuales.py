import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Configurar el generador de números aleatorios para reproducibilidad
np.random.seed(42)

# Generar fechas para 12 meses
start_date = datetime(2025, 1, 1)
dates = [start_date + timedelta(days=30 * i) for i in range(12)]  # Aproximadamente 30 días por mes

# Tipos de premios
prize_types = ['Boleto']

# Función para generar ventas con tendencia y estacionalidad
def generate_sales(base, trend, seasonality, noise_level, periods):
    t = np.arange(periods)
    trend_component = trend * t
    seasonality_component = seasonality * np.sin(2 * np.pi * t / periods)
    noise = np.random.normal(0, noise_level, periods)
    sales = base + trend_component + seasonality_component + noise
    return np.maximum(sales, 0)  # Asegurar que no haya ventas negativas

# Generar datos para cada tipo de premio para 12 meses
periods = 12
data = {
    'Fecha': dates,
    'Boleto': generate_sales(1000, 10, 100, 50, periods),
}

# Crear DataFrame
df = pd.DataFrame(data)

# Calcular ventas totales
df['Ventas Totales'] = df[prize_types].sum(axis=1)

# Añadir algo de interacción entre los tipos de premios
for i in range(1, len(prize_types)):
    df[prize_types[i]] += 0.1 * df[prize_types[i-1]]

# Recalcular ventas totales después de la interacción
df['Ventas Totales'] = df[prize_types].sum(axis=1)

# Guardar como Excel
excel_file = 'lottery_sales_data_months.xlsx'
df.to_excel(excel_file, index=False)

print(f"Datos de prueba generados y guardados en '{excel_file}'")

# Mostrar las primeras filas y estadísticas básicas
print("\nPrimeras filas del conjunto de datos:")
print(df.head())

print("\nEstadísticas básicas:")
print(df.describe())

print("\nCorrelaciones entre tipos de premios:")
print(df[prize_types + ['Ventas Totales']].corr())
