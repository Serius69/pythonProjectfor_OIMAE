import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats


# Función para cargar y preprocesar los datos
def load_and_preprocess_data(file_path):
    df = pd.read_excel(file_path)
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    return df


# Función para realizar el análisis de sensibilidad
def sensitivity_analysis(df):
    prize_types = df.columns[1:]  # Asumiendo que la primera columna es 'Date'
    sensitivities = {}

    for prize in prize_types:
        # Calcular la elasticidad de la demanda
        pct_change = df[prize].pct_change()
        total_sales_pct_change = df['Ventas Totales'].pct_change()
        elasticity = pct_change / total_sales_pct_change

        # Calcular estadísticas de sensibilidad
        sensitivities[prize] = {
            'mean': np.mean(elasticity),
            'median': np.median(elasticity),
            'std': np.std(elasticity),
            'skew': stats.skew(elasticity.dropna()),
            'kurtosis': stats.kurtosis(elasticity.dropna())
        }

    return pd.DataFrame(sensitivities).T


# Función para crear la visualización
def create_visualization(df, sensitivities):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12), gridspec_kw={'height_ratios': [2, 1]})

    # Gráfico de área apilada
    df.set_index('Fecha').plot(kind='area', stacked=True, ax=ax1, alpha=0.8)
    ax1.set_title('Comportamiento de venta de los boletos', fontsize=16)
    ax1.set_xlabel('Meses de un año', fontsize=12)
    ax1.set_ylabel('Cantidad vendida', fontsize=12)
    ax1.legend(title='Colores: Los premios', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Gráfico de barras para sensibilidades
    sensitivities['mean'].plot(kind='bar', ax=ax2, yerr=sensitivities['std'], capsize=5)
    ax2.set_title('Sensibilidad media por tipo de premio', fontsize=16)
    ax2.set_xlabel('Tipo de premio', fontsize=12)
    ax2.set_ylabel('Sensibilidad media', fontsize=12)
    ax2.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    return fig


# Función principal
def main(file_path):
    # Cargar y preprocesar datos
    df = load_and_preprocess_data(file_path)

    # Realizar análisis de sensibilidad
    sensitivities = sensitivity_analysis(df)

    # Crear visualización
    fig = create_visualization(df, sensitivities)

    # Guardar resultados
    fig.savefig('lottery_ticket_sensitivity_analysis.png', dpi=300, bbox_inches='tight')
    sensitivities.to_csv('lottery_ticket_sensitivities.csv')

    print(
        "Análisis completado. Resultados guardados en 'lottery_ticket_sensitivity_analysis.png' y 'lottery_ticket_sensitivities.csv'")


# Ejecutar el script
if __name__ == "__main__":
    file_path = "lottery_sales_data.xlsx"  # Reemplaza esto con la ruta real de tu archivo
    main(file_path)