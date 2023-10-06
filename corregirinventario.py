import streamlit as st
import sqlite3

# Conectarse a la base de datos SQLite
conn = sqlite3.connect('inventario.db')
cursor = conn.cursor()

# Crear una función para actualizar la cantidad de stock
def actualizar_stock(nombre_producto, nueva_cantidad):
    try:
        # Obtener el código del producto a partir del nombre
        cursor.execute("SELECT Codigo FROM Productos WHERE Nombre=?", (nombre_producto,))
        codigo_producto = cursor.fetchone()

        if codigo_producto:
            # Actualizar la cantidad de stock en la tabla Inventario
            cursor.execute("UPDATE Inventario SET Cantidad_Stock=? WHERE Codigo=?", (nueva_cantidad, codigo_producto[0]))
            conn.commit()
            st.success(f"Stock actualizado con éxito para {nombre_producto}.")
        else:
            st.error(f"No se encontró el producto {nombre_producto}.")

    except sqlite3.Error as e:
        st.error("Error al actualizar el stock: " + str(e))

# Crear la aplicación Streamlit
st.title("Actualización de Stock")

# Crear un formulario para ingresar el nombre del producto y la nueva cantidad de stock
nombre_producto = st.text_input("Nombre del Producto:")
nueva_cantidad = st.number_input("Nueva Cantidad de Stock:")

if st.button("Actualizar Stock"):
    if nombre_producto and nueva_cantidad:
        actualizar_stock(nombre_producto, nueva_cantidad)

# Cerrar la conexión a la base de datos al finalizar la aplicación
conn.close()
