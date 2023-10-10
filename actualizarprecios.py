import sqlite3
import csv

# Conexión a la base de datos SQLite
conexion = sqlite3.connect('inventario.db')
cursor = conexion.cursor()

# Nombre del archivo CSV
archivo_csv = 'tatito.csv'

try:
    # Abrir el archivo CSV y leer los datos
    with open(archivo_csv, 'r', newline='', encoding='utf-8') as archivo:
        lector_csv = csv.DictReader(archivo, delimiter=';')
        
        for fila in lector_csv:
            nombre_producto_csv = fila['Nombre']
            precio_venta_csv = fila['Precio_Venta'].replace('.', '').replace(',', '.')
            
            # Consulta para actualizar el Precio_Venta en la tabla Productos
            cursor.execute(
                "UPDATE Productos SET Precio_Venta = ? WHERE Nombre = ?",
                (precio_venta_csv, nombre_producto_csv)
            )

    # Guardar los cambios en la base de datos
    conexion.commit()
    print("Actualización completada correctamente.")
    
except Exception as e:
    conexion.rollback()  # En caso de error, deshacer cualquier cambio pendiente en la base de datos
    print(f"Error: {str(e)}")

finally:
    # Cerrar la conexión con la base de datos
    conexion.close()
