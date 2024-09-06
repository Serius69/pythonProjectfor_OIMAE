# main.py
from preprocesamiento import (
    cargar_encuestas, procesar_datos,
    cargar_respuestas_base, procesar_respuestas
)
from modelo import crear_modelo, entrenar_modelo, generar_respuesta
from visualizacion import visualizar_modelo, visualizar_interacciones, visualizar_resultados

import tensorflow as tf

def main():
    # --- Procesamiento de Encuestas ---
    encuestas = cargar_encuestas()
    X_train_enc, y_train_enc, tokenizer_enc, max_len_enc = procesar_datos(encuestas)
    print(f"X_train_enc shape: {X_train_enc.shape}")  # Debe ser (n_samples, max_len-1)
    print(f"y_train_enc shape: {y_train_enc.shape}")  # Debe ser (n_samples,)

    # Crear y entrenar el modelo para encuestas
    vocab_size_enc = 1000  # Debe coincidir con num_words en procesar_datos
    model_enc = crear_modelo(max_len_enc, vocab_size_enc)
    entrenar_modelo(model_enc, X_train_enc, y_train_enc, epochs=20, batch_size=16)

    # Generar nueva encuesta
    seed_text_enc = "¿Cuál es"
    nueva_encuesta = generar_respuesta(model_enc, tokenizer_enc, seed_text_enc, max_len_enc)
    print("Nueva encuesta generada:", nueva_encuesta)

    # --- Procesamiento de Respuestas ---
    respuestas_base = cargar_respuestas_base()
    X_train_res, y_train_res, tokenizer_res, max_len_res = procesar_respuestas(respuestas_base)
    print(f"X_train_res shape: {X_train_res.shape}")  # Debe ser (n_samples, max_len-1)
    print(f"y_train_res shape: {y_train_res.shape}")  # Debe ser (n_samples, vocab_size)

    # Crear y entrenar el modelo para respuestas
    vocab_size_res = len(tokenizer_res.word_index) + 1
    model_res = crear_modelo(max_len_res, vocab_size_res)
    entrenar_modelo(model_res, X_train_res, y_train_res, epochs=100, batch_size=16)

    # Generar nuevas respuestas
    num_respuestas_generar = 1000
    respuestas_generadas = []
    for i in range(num_respuestas_generar):
        seed_text = respuestas_base[i % len(respuestas_base)]  # Usar respuestas existentes como semillas
        respuesta = generar_respuesta(model_res, tokenizer_res, seed_text, max_len_res)
        respuestas_generadas.append(respuesta)
    print(f"Se generaron {len(respuestas_generadas)} respuestas.")

    # --- Visualización ---
    # Visualizar la arquitectura del modelo de encuestas
    visualizar_modelo(model_enc, 'modelo_encuestas.png')

    # Visualizar la arquitectura del modelo de respuestas
    visualizar_modelo(model_res, 'modelo_respuestas.png')

    # Visualizar interacciones de las capas para el modelo de respuestas
    visualizar_interacciones(model_res, X_train_res)

    # Visualizar resultados de las respuestas generadas
    visualizar_resultados(respuestas_generadas)

if __name__ == "__main__":
    main()
