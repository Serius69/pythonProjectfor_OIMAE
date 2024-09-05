# visualizacion.py
from tensorflow.keras.utils import plot_model
import matplotlib.pyplot as plt
import numpy as np


def visualizar_modelo(model):
    plot_model(model, to_file='modelo_red_neuronal.png', show_shapes=True, show_layer_names=True)


def visualizar_interacciones(model, X_train):
    layer_outputs = [layer.output for layer in model.layers]
    activation_model = tf.keras.models.Model(inputs=model.input, outputs=layer_outputs)
    activations = activation_model.predict(X_train[:1])

    layer_names = [layer.name for layer in model.layers]

    for layer_name, layer_activation in zip(layer_names, activations):
        n_features = layer_activation.shape[-1]
        size = layer_activation.shape[1]

        n_cols = 8
        n_rows = n_features // n_cols
        display_grid = np.zeros((size * n_rows, size * n_cols))

        for col in range(n_cols):
            for row in range(n_rows):
                channel_image = layer_activation[0, :, :, col * n_cols + row]
                channel_image -= channel_image.mean()
                channel_image /= channel_image.std()
                channel_image *= 64
                channel_image += 128
                channel_image = np.clip(channel_image, 0, 255).astype('uint8')
                display_grid[row * size: (row + 1) * size, col * size: (col + 1) * size] = channel_image

        plt.figure(figsize=(n_cols, n_rows))
        plt.title(layer_name)
        plt.imshow(display_grid, aspect='auto', cmap='viridis')
        plt.show()
