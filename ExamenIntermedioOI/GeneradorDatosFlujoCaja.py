# generadordlujocaja
import pandas as pd

# Datos de prueba: VAN en función del precio del boleto (columnas) y la cantidad vendida (filas)
data = {
    '2.5': [-375, -325, -275, -225, -175],  # Precio de boleto 2.5Bs
    '5': [-325, -255, -185, -115, -45],   # Precio de boleto 5Bs
    '10': [-275, -185, -95, -5, 85],       # Precio de boleto 10Bs
    '15': [-225, -115, -5, 105, 215],      # Precio de boleto 15Bs
    '20': [-175, -45, 85, 215, 345],       # Precio de boleto 20Bs
    '25': [-125, 25, 175, 325, 475],       # Precio de boleto 25Bs
    '30': [-75, 75, 225, 375, 525],        # Precio de boleto 30Bs
    '35': [-25, 125, 275, 425, 575],       # Precio de boleto 35Bs
    '40': [25, 175, 325, 475, 625]        # Precio de boleto 40Bs
}

# Crear el DataFrame
df = pd.DataFrame(data, index=[50000, 70000, 90000, 110000, 130000])  # Monto vendido [$ mil]

# Guardar el DataFrame en un archivo Excel
df.to_excel('data_prueba_sensibilidad.xlsx')

print("Archivo de datos de prueba creado: 'data_prueba_sensibilidad.xlsx'")
