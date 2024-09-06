import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Configurar el generador de números aleatorios para reproducibilidad
np.random.seed(42)

# Generar fechas para un año
start_date = datetime(2023, 1, 1)
dates = [start_date + timedelta(days=i) for i in range(365)]

# Tipos de premios
prize_types = ['Primer Premio', 'Segundo Premio', 'Tercer Premio', 'Cuarto Premio', 'Quinto Premio']

# Función para generar ventas con tendencia y estacionalidad
def generate_sales(base, trend, seasonality, noise_level):
    t = np.arange(365)
    trend_component = trend * t
    seasonality_component = seasonality * np.sin(2 * np.pi * t / 365)
    noise = np.random.normal(0, noise_level, 365)
    sales = base + trend_component + seasonality_component + noise
    return np.maximum(sales, 0)  # Asegurar que no haya ventas negativas

# Generar datos para cada tipo de premio
data = {
    'Fecha': dates,
    'Primer Premio': generate_sales(1000, 0.5, 100, 50),
    'Segundo Premio': generate_sales(800, 0.3, 80, 40),
    'Tercer Premio': generate_sales(600, 0.2, 60, 30),
    'Cuarto Premio': generate_sales(400, 0.1, 40, 20),
    'Quinto Premio': generate_sales(200, 0.05, 20, 10)
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
excel_file = 'lottery_sales_data.xlsx'
df.to_excel(excel_file, index=False)

print(f"Datos de prueba generados y guardados en '{excel_file}'")

# Mostrar las primeras filas y estadísticas básicas
print("\nPrimeras filas del conjunto de datos:")
print(df.head())

print("\nEstadísticas básicas:")
print(df.describe())

print("\nCorrelaciones entre tipos de premios:")
print(df[prize_types + ['Ventas Totales']].corr())