# modelo.py
import numpy as np
import tensorflow as tf
from keras.src.utils import pad_sequences


def crear_modelo(max_len):
    embedding_dim = 64
    lstm_units = 128

    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(input_dim=1000, output_dim=embedding_dim, input_length=max_len),
        tf.keras.layers.LSTM(lstm_units, return_sequences=True),
        tf.keras.layers.LSTM(lstm_units),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(1000, activation='softmax')
    ])

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model


def entrenar_modelo(model, X_train, y_train, epochs=50, batch_size=16):
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size)


def generar_encuesta(model, tokenizer, seed_text, max_len, num_words):
    for _ in range(num_words):
        tokenized_seed = tokenizer.texts_to_sequences([seed_text])[0]
        tokenized_seed = pad_sequences([tokenized_seed], maxlen=max_len - 1, padding='post')
        predicted = np.argmax(model.predict(tokenized_seed), axis=-1)

        for word, index in tokenizer.word_index.items():
            if index == predicted:
                seed_text += " " + word
                break
    return seed_text
