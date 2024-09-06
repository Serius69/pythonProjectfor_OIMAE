# preprocesamiento.py
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import tensorflow as tf

def cargar_encuestas():
    encuestas = [
        "Fecha",
        "Género",
        "¿Vives en una zona urbana o rural?",
        "¿Has participado alguna vez en una lotería?",
        "Si tu respuesta es Sí, ¿Con qué frecuencia participas?",
        "Si no juegas actualmente, ¿Qué haría que te interesaras en participar en una lotería?",
        "¿Qué te motiva a participar en una lotería?",
        "¿Qué tipo de lotería te atrae más?",
        "¿Qué canal prefieres para comprar tus boletos?",
        "¿Cuánto estarías dispuesto a gastar en boletos de lotería por mes?",
    ]
    return encuestas

def procesar_datos(encuestas, num_words=1000):
    tokenizer = Tokenizer(num_words=num_words, oov_token="<OOV>")
    tokenizer.fit_on_texts(encuestas)
    sequences = tokenizer.texts_to_sequences(encuestas)

    # Aseguramos que las secuencias tengan el mismo tamaño
    max_len = max([len(seq) for seq in sequences])
    padded_sequences = pad_sequences(sequences, maxlen=max_len, padding='post')

    # X_train será el texto (todas las palabras menos la última)
    X_train = padded_sequences[:, :-1]  # Todas las palabras menos la última
    # y_train será la última palabra en la secuencia (es decir, el siguiente token a predecir)
    y_train = padded_sequences[:, -1]  # La última palabra de cada secuencia

    return X_train, y_train, tokenizer, max_len

def cargar_respuestas_base():
    respuestas_base = [
        "9/4/2024 12:06:00",
        "Mujer",
        "Urbana",
        "Cochabamba",
        "Si",
        "Raramente",
        "Ofertas y descuentos en boletos.",
        "La posibilidad de ganar grandes premios.",
        "9/4/2024 12:06:00",
        "Participaré en la lotería con frecuencia",
        "Espero tener buena suerte",
        "Quiero mejorar mis posibilidades de ganar",
        # Añadir hasta tener 80 respuestas
    ]
    return respuestas_base

def procesar_respuestas(respuestas_base, num_words=1000):
    tokenizer = Tokenizer(num_words=num_words, oov_token="<OOV>")
    tokenizer.fit_on_texts(respuestas_base)
    sequences = tokenizer.texts_to_sequences(respuestas_base)

    # Rellenar las secuencias para que tengan el mismo tamaño
    max_sequence_len = max([len(x) for x in sequences])
    padded_sequences = pad_sequences(sequences, maxlen=max_sequence_len, padding='post')

    # Datos y etiquetas para entrenar el modelo
    X = padded_sequences[:, :-1]
    y = padded_sequences[:, -1]
    y = tf.keras.utils.to_categorical(y, num_classes=len(tokenizer.word_index) + 1)

    return X, y, tokenizer, max_sequence_len
