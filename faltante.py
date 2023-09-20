import streamlit as st
import sqlite3

# Función para conectar a la base de datos SQLite
def connect_db():
    return sqlite3.connect('inventario.db')

# Función para buscar el producto por código
def buscar_producto_por_codigo(codigo):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT Nombre FROM Productos WHERE Codigo = ?", (codigo,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

# Función para actualizar el campo Faltante en la tabla Inventario
def actualizar_faltante(codigo, faltante):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE Inventario SET Faltante = ? WHERE Codigo = ?", (faltante, codigo))
    conn.commit()
    conn.close()

# Configurar la aplicación de Streamlit
st.title("Carga de Parametros")

# Crear un formulario para ingresar el código
codigo = st.text_input("Ingrese el código del producto:")

# Botón para buscar el producto y mostrar el nombre
if st.button("Buscar"):
    if codigo:
        producto = buscar_producto_por_codigo(codigo)
        if producto:
            st.success(f"Producto encontrado: {producto[0]}")
        else:
            st.error("Producto no encontrado")

# Campo para ingresar el valor del campo Faltante
faltante = st.number_input("Ingrese el valor de Faltante:", min_value=0, step=1)

# Botón para actualizar el campo Faltante en la tabla Inventario
if st.button("Actualizar Faltante"):
    if codigo and faltante is not None:
        actualizar_faltante(codigo, faltante)
        st.success("Faltante actualizado exitosamente")

