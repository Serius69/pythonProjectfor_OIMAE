# preprocesamiento.py
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

def cargar_encuestas():
    encuestas = [
        "¿Cuál es su edad?",
        "¿Con qué frecuencia usa redes sociales?",
        "¿Qué tan satisfecho está con su trabajo?",
        "¿Cuál es su nivel de estudios?",
        # Más encuestas hasta completar 30
    ]
    return encuestas


def procesar_datos(encuestas):
    tokenizer = Tokenizer(num_words=1000, oov_token="<OOV>")
    tokenizer.fit_on_texts(encuestas)
    sequences = tokenizer.texts_to_sequences(encuestas)

    max_len = max([len(seq) for seq in sequences])
    padded_sequences = pad_sequences(sequences, maxlen=max_len, padding='post')

    X_train = padded_sequences[:, :-1]
    y_train = padded_sequences[:, 1:]

    return X_train, y_train, tokenizer, max_len
