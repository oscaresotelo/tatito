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
import sqlite3

# Conectarse a la base de datos
conexion = sqlite3.connect("inventario.db")
cursor = conexion.cursor()

# Agregar el campo FechaVto de tipo date a la tabla Inventario
try:
    cursor.execute("ALTER TABLE Inventario ADD COLUMN FechaVto DATE")
    conexion.commit()
    print("Campo FechaVto agregado exitosamente.")
except sqlite3.Error as e:
    print(f"Error al agregar el campo FechaVto: {e}")
finally:
    conexion.close()
