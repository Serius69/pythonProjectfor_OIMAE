# visualizacion.py
from tensorflow.keras.utils import plot_model
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import seaborn as sns
from collections import Counter

def visualizar_modelo(model, filename='modelo_red_neuronal.png'):
    plot_model(model, to_file=filename, show_shapes=True, show_layer_names=True)
    print(f"Arquitectura del modelo guardada en {filename}")

def visualizar_interacciones(model, X_train):
    # Asegúrate de que las capas son compatibles para visualización
    layer_outputs = [layer.output for layer in model.layers]
    activation_model = tf.keras.models.Model(inputs=model.input, outputs=layer_outputs)
    activations = activation_model.predict(X_train[:1])

    layer_names = [layer.name for layer in model.layers]

    for layer_name, layer_activation in zip(layer_names, activations):
        if len(layer_activation.shape) == 2:  # Por ejemplo, capas Dense
            plt.figure(figsize=(10, 6))
            plt.title(f'Activaciones de la capa {layer_name}')
            sns.heatmap(layer_activation, cmap='viridis')
            plt.show()
        elif len(layer_activation.shape) == 3:  # Por ejemplo, capas LSTM
            # Mostrar solo las primeras 10 características para evitar sobrecarga
            plt.figure(figsize=(10, 6))
            plt.title(f'Activaciones de la capa {layer_name}')
            sns.heatmap(layer_activation[0, :, :10], cmap='viridis')
            plt.show()

def visualizar_resultados(respuestas_generadas):
    # Distribución de la Frecuencia de Palabras
    todas_las_respuestas = ' '.join(respuestas_generadas)
    palabras = todas_las_respuestas.split()
    conteo_palabras = Counter(palabras)

    # Graficar la distribución de las 20 palabras más comunes
    plt.figure(figsize=(10,6))
    plt.bar(*zip(*conteo_palabras.most_common(20)))
    plt.title('Frecuencia de las 20 palabras más comunes')
    plt.xticks(rotation=45)
    plt.xlabel('Palabras')
    plt.ylabel('Frecuencia')
    plt.show()

    # Análisis de Tendencias en el Tiempo (Longitud de las respuestas generadas)
    plt.figure(figsize=(10,6))
    plt.plot(range(len(respuestas_generadas)), [len(resp.split()) for resp in respuestas_generadas])
    plt.title('Tendencia del Largo de las Respuestas Generadas')
    plt.xlabel('Número de respuesta')
    plt.ylabel('Número de palabras')
    plt.show()

    # Distribución de Palabras Clave Específicas
    palabras_clave = ["ganar", "premio", "lotería", "suerte"]  # Personalizar según tus necesidades
    conteo_palabras_clave = {palabra: todas_las_respuestas.split().count(palabra) for palabra in palabras_clave}

    # Gráfico de barras para palabras clave
    plt.figure(figsize=(8,6))
    sns.barplot(x=list(conteo_palabras_clave.keys()), y=list(conteo_palabras_clave.values()))
    plt.title('Distribución de Palabras Clave en Respuestas Generadas')
    plt.xlabel('Palabras Clave')
    plt.ylabel('Frecuencia')
    plt.show()
