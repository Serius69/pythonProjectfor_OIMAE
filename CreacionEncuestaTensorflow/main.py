# main.py
from preprocesamiento import cargar_encuestas, procesar_datos
from modelo import crear_modelo, entrenar_modelo, generar_encuesta
from visualizacion import visualizar_modelo, visualizar_interacciones

# Cargar y procesar los datos
encuestas = cargar_encuestas()
X_train, y_train, tokenizer, max_len = procesar_datos(encuestas)
print(f"X_train shape: {X_train.shape}")  # Debe ser (n_samples, max_len-1)
print(f"y_train shape: {y_train.shape}")  # Debe ser (n_samples, max_len-1)

# Crear el modelo
model = crear_modelo(max_len)

# Entrenar el modelo
entrenar_modelo(model, X_train, y_train)

# Generar nuevas encuestas
seed_text = "¿Cuál es"
nueva_encuesta = generar_encuesta(model, tokenizer, seed_text, max_len, num_words=5)
print("Nueva encuesta generada:", nueva_encuesta)

# Visualizar la arquitectura del modelo
visualizar_modelo(model)

# Visualizar interacciones de las capas
visualizar_interacciones(model, X_train)
