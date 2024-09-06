# modelo.py
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences

def crear_modelo(max_len, vocab_size):
    embedding_dim = 100  # Actualizado según las nuevas especificaciones
    lstm_units1 = 150
    lstm_units2 = 100

    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_len - 1),
        tf.keras.layers.LSTM(lstm_units1, return_sequences=True),
        tf.keras.layers.LSTM(lstm_units2),
        tf.keras.layers.Dense(100, activation='relu'),
        tf.keras.layers.Dense(vocab_size, activation='softmax')
    ])

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

def entrenar_modelo(model, X_train, y_train, epochs=100, batch_size=16):
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size)

def generar_respuesta(model, tokenizer, seed_text, max_sequence_len):
    for _ in range(1000):  # Genera 1000 palabras
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_len-1, padding='pre')
        predicted = np.argmax(model.predict(token_list), axis=-1)[0]  # Tomamos el primer elemento

        # Obtener la palabra correspondiente al índice predicho
        output_word = tokenizer.index_word.get(predicted, "")
        if output_word == "":
            break  # Detener si no se encuentra la palabra
        seed_text += " " + output_word
    return seed_text
