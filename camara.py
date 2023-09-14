""" import streamlit as st

from streamlit_back_camera_input import back_camera_input

image = back_camera_input()
if image:
    st.image(image) """

""" 
import streamlit as st
from streamlit_qrcode_scanner import qrcode_scanner

qr_code = qrcode_scanner(key='qrcode_scanner')

if qr_code:
    st.write(qr_code)
 """

import streamlit as st
import sqlite3
from streamlit_qrcode_scanner import qrcode_scanner

# Función para buscar en la base de datos
def buscar_producto_por_codigo(codigo):
    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Productos WHERE Codigo=?", (codigo,))
    producto = cursor.fetchone()
    conn.close()
    return producto

qr_code = qrcode_scanner(key='qrcode_scanner')

if qr_code:
    producto = buscar_producto_por_codigo(qr_code)
    if producto:
        st.write("Datos del producto:")
        st.write(f"Nombre: {producto[1]}")
        st.write(f"Descripción: {producto[2]}")
        st.write(f"Precio: {producto[3]}")
    else:
        st.write("Producto no encontrado en la base de datos.")
