# preprocesamiento.py
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


def cargar_encuestas():
    encuestas = [
        "¿Cuál es su edad?",
        "¿Con qué frecuencia usa redes sociales?",
        "¿Qué tan satisfecho está con su trabajo?",
        "¿Cuál es su nivel de estudios?",
        # Añadir más encuestas hasta llegar a 30
    ]
    return encuestas


def procesar_datos(encuestas):
    tokenizer = Tokenizer(num_words=1000, oov_token="<OOV>")
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
