# import sqlite3

# # Crear una conexión a la base de datos (creará el archivo si no existe)
# conn = sqlite3.connect('inventario.db')

# # Crear un objeto cursor para ejecutar comandos SQL
# cursor = conn.cursor()

# # Crear la tabla de Productos
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS Productos (
#         ID_Producto INTEGER PRIMARY KEY,
#         Nombre TEXT,
#         Descripcion TEXT,
#         Precio_Compra REAL,
#         Precio_Venta REAL,
#         Categoria TEXT,
#         Proveedor TEXT,
#         Unidad_Medida TEXT
#     )
# ''')

# # Crear la tabla de Inventario
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS Inventario (
#         ID_Inventario INTEGER PRIMARY KEY,
#         ID_Producto INTEGER,
#         Cantidad_Stock INTEGER,
#         Ubicacion_Almacen TEXT,
#         Fecha_Actualizacion DATE,
#         FOREIGN KEY (ID_Producto) REFERENCES Productos (ID_Producto)
#     )
# ''')

# # Crear la tabla de Movimientos de Inventario
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS Movimientos_Inventario (
#         ID_Movimiento INTEGER PRIMARY KEY,
#         ID_Producto INTEGER,
#         Tipo_Movimiento TEXT,
#         Cantidad_Movida INTEGER,
#         Fecha_Hora_Movimiento DATETIME,
#         Usuario TEXT,
#         Razon_Movimiento TEXT,
#         FOREIGN KEY (ID_Producto) REFERENCES Productos (ID_Producto)
#     )
# ''')

# # Crear la tabla de Proveedores (si es necesario)
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS Proveedores (
#         ID_Proveedor INTEGER PRIMARY KEY,
#         Nombre_Proveedor TEXT,
#         Contacto TEXT
#     )
# ''')

# # Crear la tabla de Categorías (si es necesario)
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS Categorias (
#         ID_Categoria INTEGER PRIMARY KEY,
#         Nombre_Categoria TEXT
#     )
# ''')

# # Guardar los cambios y cerrar la conexión
# conn.commit()
# conn.close()

# print("Las tablas se han creado correctamente en la base de datos SQLite3.")
import sqlite3

# Nombre de la base de datos SQLite
database_name = "inventario.db"

try:
    # Conectarse a la base de datos
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    # Consulta SQL para borrar todos los datos de la tabla Productos
    delete_query = "DELETE FROM Movimientos_inventario"

    # Ejecutar la consulta
    cursor.execute(delete_query)

    # Confirmar los cambios en la base de datos
    conn.commit()

    print("Los datos de la tabla Productos han sido eliminados correctamente.")

except sqlite3.Error as e:
    print("Error al conectar a la base de datos:", e)

finally:
    # Cerrar la conexión a la base de datos, independientemente de si se produjo un error o no
    if conn:
        conn.close()
