import streamlit as st
import sqlite3

# Conectar con la base de datos
conn = sqlite3.connect("inventario.db")
cur = conn.cursor()

# Definir el título de la aplicación
st.title("Buscar producto")

# Crear un control de entrada de texto para el nombre del producto
nombre_producto = st.text_input("Nombre del producto:")

# Si el nombre del producto no está vacío, realizar la búsqueda
if nombre_producto != "":

    # Ejecutar la consulta SQL
    cur.execute("SELECT * FROM Productos WHERE Nombre LIKE '%{}%'".format(nombre_producto))

    # Obtener los resultados de la consulta
    resultados = cur.fetchall()

    # Mostrar los resultados en una tabla
    st.table(resultados)

    # Crear un control de selección para el ID del producto
    id_producto = st.selectbox("ID del producto:", [r[0] for r in resultados])

    # Si el ID del producto no está vacío, mostrarlo
    if id_producto != "":
        st.write("ID del producto seleccionado:", id_producto)

# Cerrar la conexión con la base de datos
conn.close()
