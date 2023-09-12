
# import streamlit as st
# import sqlite3

# # Conectar con la base de datos
# conn = sqlite3.connect("inventario.db")
# cur = conn.cursor()

# # Definir el título de la aplicación
# st.markdown("<h1 style='text-align: center; color: red;'>BUSCAR PRODUCTO</h1>", unsafe_allow_html=True)

# # Crear un control de entrada de texto para el nombre del producto
# nombre_producto = st.text_input("Nombre del producto:")

# # Si el nombre del producto no está vacío, realizar la búsqueda
# if nombre_producto != "":

#     # Ejecutar la consulta SQL con un JOIN entre Productos e Inventario
#     cur.execute("""
#     SELECT P.*, I.Cantidad_Stock
#     FROM Productos AS P
#     LEFT JOIN Inventario AS I ON P.ID_Producto = I.ID_Producto
#     WHERE P.Nombre LIKE ?
#     """, ('%' + nombre_producto + '%',))

#     # Obtener los resultados de la consulta
#     resultados = cur.fetchall()

#     # Mostrar los resultados en una tabla
#     st.dataframe(resultados)

#     # Mostrar el campo "Cantidad_Stock" debajo de la tabla
#     cantidad_stock = [r[-1] for r in resultados]  # Obtener la última columna (Cantidad_Stock)
#     cantidad_stock = str(cantidad_stock)
#     st.write("Stock Restante: " + str(cantidad_stock))

# # Cerrar la conexión con la base de datos
# conn.close()
import streamlit as st
import sqlite3
import pandas as pd

# Conectar con la base de datos
conn = sqlite3.connect("inventario.db")
cur = conn.cursor()

# Definir el título de la aplicación
st.markdown("<h1 style='text-align: center; color: red;'>BUSCAR PRODUCTO</h1>", unsafe_allow_html=True)

# Crear un control de entrada de texto para el nombre del producto
nombre_producto = st.text_input("Nombre del producto:")

# Si el nombre del producto no está vacío, realizar la búsqueda
if nombre_producto != "":

    # Ejecutar la consulta SQL con un JOIN entre Productos e Inventario
    cur.execute("""
    SELECT P.Nombre AS Nombre_Producto, P.Precio_Venta, I.Cantidad_Stock
    FROM Productos AS P
    LEFT JOIN Inventario AS I ON P.ID_Producto = I.ID_Producto
    WHERE P.Nombre LIKE ?
    """, ('%' + nombre_producto + '%',))

    # Obtener los resultados de la consulta
    resultados = cur.fetchall()

    # Crear un DataFrame a partir de los resultados
    df = pd.DataFrame(resultados, columns=["Nombre del Producto", "Precio", "Stock Restante"])

    # Mostrar los resultados en una tabla
    st.dataframe(df)

    # Mostrar el campo "Cantidad_Stock" debajo de la tabla
    cantidad_stock = df["Stock Restante"].sum()
    st.write("Stock Restante Total: " + str(cantidad_stock))

# Cerrar la conexión con la base de datos
conn.close()
