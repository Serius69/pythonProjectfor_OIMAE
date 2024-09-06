import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats


def load_and_preprocess_data(file_path):
    df = pd.read_excel(file_path)
    print("Columnas en el DataFrame:")
    print(df.columns)
    return df


def get_boletos_columns(df):
    boletos_columns = [col for col in df.columns if 'Boletos Vendidos' in col]
    if len(boletos_columns) < 2:
        raise ValueError(
            f"No se encontraron suficientes columnas de 'Boletos Vendidos'. Columnas encontradas: {boletos_columns}")
    return boletos_columns


def get_total_column(df):
    total_column = [col for col in df.columns if 'Total' in col and 'Boletos' in col]
    if not total_column:
        raise ValueError("No se encontró la columna de total de boletos.")
    return total_column[0]


def sensitivity_analysis(df, boletos_columns, total_column):
    sensitivities = {}
    for prize in boletos_columns:
        pct_change = df[prize].pct_change()
        total_sales_pct_change = df[total_column].pct_change()
        elasticity = pct_change / total_sales_pct_change
        sensitivities[prize] = {
            'mean': np.mean(elasticity),
            'median': np.median(elasticity),
            'std': np.std(elasticity),
            'skew': stats.skew(elasticity.dropna()),
            'kurtosis': stats.kurtosis(elasticity.dropna())
        }
    return pd.DataFrame(sensitivities).T


def create_visualization(df, sensitivities, boletos_columns):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12), gridspec_kw={'height_ratios': [2, 1]})
    df.set_index('Fecha')[boletos_columns].plot(kind='area', stacked=True, ax=ax1, alpha=0.8)
    ax1.set_title('Comportamiento de venta de los boletos', fontsize=16)
    ax1.set_xlabel('Meses de un año', fontsize=12)
    ax1.set_ylabel('Cantidad vendida', fontsize=12)
    ax1.legend(title='Tipos de Lotería', bbox_to_anchor=(1.05, 1), loc='upper left')
    sensitivities['mean'].plot(kind='bar', ax=ax2, yerr=sensitivities['std'], capsize=5)
    ax2.set_title('Sensibilidad media por tipo de lotería', fontsize=16)
    ax2.set_xlabel('Tipo de lotería', fontsize=12)
    ax2.set_ylabel('Sensibilidad media', fontsize=12)
    ax2.tick_params(axis='x', rotation=45)
    plt.tight_layout()
    return fig


def plot_line_chart(df, boletos_columns):
    plt.figure(figsize=(12, 6))
    for col in boletos_columns:
        plt.plot(df['Fecha'], df[col], label=col)
    plt.title('Evolución de Ventas de Boletos a lo Largo del Tiempo')
    plt.xlabel('Fecha')
    plt.ylabel('Cantidad Vendida')
    plt.legend()
    plt.tight_layout()
    plt.savefig('2_evolucion_ventas.png')
    plt.close()


def plot_pie_chart(df, boletos_columns):
    total_sales = df[boletos_columns].sum()
    plt.figure(figsize=(8, 8))
    plt.pie(total_sales, labels=total_sales.index, autopct='%1.1f%%')
    plt.title('Participación en Ventas Totales')
    plt.savefig('3_participacion_ventas.png')
    plt.close()


def plot_scatter(df, boletos_columns, total_column):
    plt.figure(figsize=(10, 6))
    for col in boletos_columns:
        plt.scatter(df[total_column], df[col], label=col, alpha=0.5)
    plt.title('Relación entre Ventas Totales y Ventas por Lotería')
    plt.xlabel(total_column)
    plt.ylabel('Boletos Vendidos por Lotería')
    plt.legend()
    plt.savefig('4_ventas_totales_vs_individuales.png')
    plt.close()


def plot_heatmap(df, boletos_columns, total_column):
    correlation_matrix = df[boletos_columns + [total_column]].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
    plt.title('Correlaciones entre Variables')
    plt.tight_layout()
    plt.savefig('6_heatmap_correlaciones.png')
    plt.close()


def plot_market_share(df, boletos_columns, total_column):
    for col in boletos_columns:
        df[f'Cuota {col}'] = df[col] / df[total_column]
    plt.figure(figsize=(12, 6))
    for col in boletos_columns:
        plt.plot(df['Fecha'], df[f'Cuota {col}'], label=col)
    plt.title('Evolución de la Cuota de Mercado')
    plt.xlabel('Fecha')
    plt.ylabel('Cuota de Mercado')
    plt.legend()
    plt.tight_layout()
    plt.savefig('7_cuota_mercado.png')
    plt.close()


def main(file_path):
    try:
        df = load_and_preprocess_data(file_path)
        boletos_columns = get_boletos_columns(df)
        total_column = get_total_column(df)

        sensitivities = sensitivity_analysis(df, boletos_columns, total_column)
        fig = create_visualization(df, sensitivities, boletos_columns)
        fig.savefig('lottery_ticket_sensitivity_analysis_2024.png', dpi=300, bbox_inches='tight')
        sensitivities.to_csv('lottery_ticket_sensitivities.csv')

        plot_line_chart(df, boletos_columns)
        plot_pie_chart(df, boletos_columns)
        plot_scatter(df, boletos_columns, total_column)
        plot_heatmap(df, boletos_columns, total_column)
        plot_market_share(df, boletos_columns, total_column)

        print("Análisis completado. Todos los gráficos han sido generados y guardados como archivos PNG.")
    except Exception as e:
        print(f"Error durante el análisis: {str(e)}")
        print("Columnas disponibles en el DataFrame:")
        print(df.columns if 'df' in locals() else "DataFrame no cargado")


if __name__ == "__main__":
    file_path = "lottery_sales_data_months - 2026.xlsx"
    main(file_path)