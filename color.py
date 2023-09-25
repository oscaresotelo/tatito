# import sqlite3

# # Conectarse a la base de datos inventario.db
# conexion_inventario = sqlite3.connect('inventario.db')
# cursor_inventario = conexion_inventario.cursor()

# # Copiar los datos de la tabla Basesuper a la tabla Productos
# consulta_copia = '''
# INSERT INTO Productos (Codigo, Nombre, Rubro, Subrubro)
# SELECT CAST(Codigo AS INTEGER), Descripcion, CAST(Rubro AS INTEGER), CAST(Subrubro AS INTEGER)
# FROM Basesuper;
# '''

# cursor_inventario.execute(consulta_copia)
# conexion_inventario.commit()

# # Cerrar la conexión
# conexion_inventario.close()
import sqlite3

# Conectarse a la base de datos
conexion = sqlite3.connect('inventario.db')
cursor = conexion.cursor()

# Encontrar los registros duplicados en el campo Codigo
cursor.execute("SELECT Codigo FROM Productos GROUP BY Codigo HAVING COUNT(*) > 1")
codigos_duplicados = cursor.fetchall()

# Eliminar el segundo registro duplicado en cada grupo
for codigo in codigos_duplicados:
    cursor.execute("""
        DELETE FROM Productos
        WHERE Codigo = ?
        AND ROWID NOT IN (
            SELECT MIN(ROWID)
            FROM Productos
            WHERE Codigo = ?
        )
    """, (codigo[0], codigo[0]))
    conexion.commit()

# Cerrar la conexión
conexion.close()
