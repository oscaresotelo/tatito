# import csv
# import sqlite3

# # Nombre de la base de datos SQLite
# database_name = "inventario.db"

# try:
#     # Conectarse a la base de datos
#     conn = sqlite3.connect(database_name)
#     cursor = conn.cursor()

#     # Crear la tabla Productos si no existe
#     create_table_query = '''
#     CREATE TABLE IF NOT EXISTS Productos (
#         ID_Producto INTEGER PRIMARY KEY AUTOINCREMENT,
#         Codigo INTEGER,
#         Descripcion TEXT,
#         Rubro INTEGER,
#         Subrubro INTEGER
#     )
#     '''
#     cursor.execute(create_table_query)

#     # Abrir y leer el archivo CSV
#     with open("basesuper.csv", "r") as csv_file:
#         csv_reader = csv.DictReader(csv_file)
        
#         for row in csv_reader:
#             # Insertar cada fila en la tabla Productos
#             cursor.execute("INSERT INTO Productos (Codigo, Nombre, Rubro, Subrubro) VALUES (?, ?, ?, ?)",
#                            (str(row["Codigo"]), row["Nombre"], str(row["Rubro"]), str(row["Subrubro"])))

#     # Confirmar los cambios en la base de datos
#     conn.commit()

#     print("Los datos se han importado correctamente.")

# except sqlite3.Error as e:
#     print("Error al conectar a la base de datos:", e)

# finally:
#     # Cerrar la conexión a la base de datos, independientemente de si se produjo un error o no
#     if conn:
#         conn.close()
# import csv
# import sqlite3

# # Nombre de la base de datos SQLite
# database_name = "inventario.db"

# try:
#     # Conectarse a la base de datos
#     conn = sqlite3.connect(database_name)
#     cursor = conn.cursor()

#     # Crear la tabla Productos si no existe
#     create_table_query = '''
#     CREATE TABLE IF NOT EXISTS Productos (
#         ID_Producto INTEGER PRIMARY KEY AUTOINCREMENT,
#         Codigo INTEGER,
#         Descripcion TEXT,
#         Rubro INTEGER,
#         Subrubro INTEGER
#     )
#     '''
#     cursor.execute(create_table_query)

#     # Abrir y leer el archivo CSV
#     with open("basesuper.csv", "r") as csv_file:
#         csv_reader = csv.DictReader(csv_file)
        
#         for row in csv_reader:
#             # Insertar cada fila en la tabla Productos sin incluir el campo ID_Producto
#             cursor.execute("INSERT INTO Productos (Codigo, Nombre, Rubro, Subrubro) VALUES (?, ?, ?, ?)",
#                            (str(row["Codigo"]), row["Nombre"], str(row["Rubro"]), str(row["Subrubro"])))

#     # Confirmar los cambios en la base de datos
#     conn.commit()

#     print("Los datos se han importado correctamente.")

# except sqlite3.Error as e:
#     print("Error al conectar a la base de datos:", e)

# finally:
#     # Cerrar la conexión a la base de datos, independientemente de si se produjo un error o no
#     if conn:
#         conn.close()
# import sqlite3

# # Nombre de la base de datos SQLite
# database_name = "inventario.db"

# try:
#     # Conectarse a la base de datos
#     conn = sqlite3.connect(database_name)
#     cursor = conn.cursor()

#     # Consulta SQL para obtener el valor actual de ID_Producto
#     cursor.execute("SELECT MAX(ID_Producto) FROM Productos")
#     max_id = cursor.fetchone()[0]

#     if max_id is not None:
#         # Actualizar el campo ID_Producto sumando 1
#         cursor.execute(f"UPDATE Productos SET ID_Producto = ID_Producto + {max_id + 1}")

#         # Confirmar los cambios en la base de datos
#         conn.commit()

#         print("Se ha actualizado el campo ID_Producto correctamente.")

#     else:
#         print("La tabla Productos está vacía.")

# except sqlite3.Error as e:
#     print("Error al conectar a la base de datos:", e)

# finally:
#     # Cerrar la conexión a la base de datos, independientemente de si se produjo un error o no
#     if conn:
#         conn.close()
# import sqlite3

# # Conectarse a la base de datos
# conexion = sqlite3.connect("inventario.db")
# cursor = conexion.cursor()

# # Agregar el campo FechaVto de tipo date a la tabla Inventario
# try:
#     cursor.execute("ALTER TABLE Inventario ADD COLUMN FechaVto DATE")
#     conexion.commit()
#     print("Campo FechaVto agregado exitosamente.")
# except sqlite3.Error as e:
#     print(f"Error al agregar el campo FechaVto: {e}")
# finally:
#     conexion.close()
# import sqlite3

# # Conectarse a la base de datos
# conexion = sqlite3.connect("inventario.db")
# cursor = conexion.cursor()

# # Consulta SQL para cambiar el tipo de dato de los campos "Cambio" y "FechaVto"
# consulta = """
#     PRAGMA foreign_keys=off;

#     -- Crear una tabla temporal con la nueva estructura
#     CREATE TABLE Temp_Movimiento_Inventario AS
#     SELECT
#         ID_Movimiento,
#         Codigo,
#         Tipo_Movimiento,
#         Cantidad_Movida,
#         Fecha_Hora_Movimiento,
#         Usuario,
#         Razon_Movimiento,
#         CAST(Cambio AS REAL) AS Cambio,  -- Cambiar el tipo de dato a REAL
#         CAST(FechaVto AS DATE) AS FechaVto  -- Cambiar el tipo de dato a DATE
#     FROM Movimiento_Inventario;

#     -- Eliminar la tabla original
#     DROP TABLE Movimiento_Inventario;

#     -- Renombrar la tabla temporal
#     ALTER TABLE Temp_Movimiento_Inventario RENAME TO Movimiento_Inventario;

#     PRAGMA foreign_keys=on;
# """

# # Ejecutar la consulta
# cursor.executescript(consulta)

# # Confirmar los cambios y cerrar la conexión
# conexion.commit()
# conexion.close()
# import sqlite3

# # Conectarse a la base de datos
# conexion = sqlite3.connect("inventario.db")
# cursor = conexion.cursor()

# # Actualizar los registros vacíos en "Precio_Compra" y "Precio_Venta"
# query = "UPDATE productos SET Cantidad_Medida = 1.0 WHERE Cantidad_Medida IS NULL "
# cursor.execute(query)

# # Guardar los cambios en la base de datos
# conexion.commit()

# # Cerrar la conexión
# conexion.close()

# import sqlite3

# # Conectar a la base de datos SQLite
# conexion = sqlite3.connect('inventario.db')
# cursor = conexion.cursor()

# # Borrar todos los datos de la tabla "Inventario"
# cursor.execute('DELETE FROM Movimiento_Inventario')

# # Confirmar los cambios y cerrar la conexión
# conexion.commit()
# conexion.close()

# print("Todos los datos de la tabla Inventario han sido eliminados.")

import sqlite3
import csv

# Conectarse a la base de datos
conn = sqlite3.connect('inventario.db')
cursor = conn.cursor()

# Consulta SQL para obtener los datos necesarios
query = """
    SELECT MI.*, P.Nombre
    FROM Movimiento_Inventario AS MI
    JOIN Productos AS P ON MI.Codigo = P.Codigo
    WHERE MI.Tipo_Movimiento = 'Salida'
"""

# Ejecutar la consulta
cursor.execute(query)

# Obtener todos los registros
rows = cursor.fetchall()

# Cerrar la conexión a la base de datos
conn.close()

# Exportar los datos a un archivo CSV con codificación utf-8
with open('movimiento_salida.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    
    # Escribir encabezados
    csv_writer.writerow([i[0] for i in cursor.description])
    
    # Escribir los datos
    csv_writer.writerows(rows)

print("Los datos se han exportado correctamente a movimiento_salida.csv")
