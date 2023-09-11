import streamlit as st
import sqlite3

# Conectar con la base de datos
conn = sqlite3.connect("inventario.db")
cur = conn.cursor()

# Definir el título de la aplicación
st.title("Cargar categorías")

# Crear un control de entrada de texto para el nombre de la categoría
nombre_categoria = st.text_input("Nombre de la categoría:")

# Si el nombre de la categoría no está vacío, cargar los datos
if nombre_categoria != "":

    # Insertar el registro en la tabla
    cur.execute("INSERT INTO Categorias (Nombre_Categoria) VALUES ('{}')".format(nombre_categoria))

    # Actualizar la base de datos
    conn.commit()

    # Mostrar lo que se cargó
    st.write("Se cargó la siguiente categoría:")
    st.write("ID:", cur.lastrowid)
    st.write("Nombre:", nombre_categoria)

# Cerrar la conexión con la base de datos
conn.close()
