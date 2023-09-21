import streamlit as st
import sqlite3
from streamlit_qrcode_scanner import qrcode_scanner
import datetime


hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
                     .container {
                display: flex;
            }
            .logo-text {
                font-weight:700 !important;
                font-size:30px !important;
                color: black !important;
                padding-top: 50px !important;
            }
            .logo-img {
                float:right;
            }
            </style>
            """
st.markdown(hide_st_style, 

    unsafe_allow_html=True)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
local_css("estilos.css")


# Función para conectar a la base de datos SQLite

if "ingreso" not in st.session_state:
      st.session_state.ingreso = ""


if st.session_state.ingreso == "":
    st.warning("Por favor Ingrese Correctamente")
else:
    st.markdown("<h1 style='text-align: center; color: red;'>Carga de Parametros</h1>", unsafe_allow_html=True)
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
    def buscar_producto_por_codigo(codigo):
        conn = sqlite3.connect("inventario.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.Nombre, r.NombreRubro, p.Precio_Venta
            FROM Productos p
            INNER JOIN Rubros r ON p.Rubro = r.CodRubro
            WHERE p.Codigo=?
        """, (codigo,))
        producto = cursor.fetchone()
        conn.close()
        return producto

    qr_code = qrcode_scanner(key='qrcode_scanner')

    # Configurar la aplicación de Streamlit

    if qr_code:
            producto = buscar_producto_por_codigo(qr_code)
            if producto:
                st.write(qr_code)
                st.write("Datos del producto:")
                st.write(f"Nombre: {producto[0]}")
                st.write(f"Rubro: {producto[1]}")
                st.write(f"Precio: {producto[2]}")

    faltante = st.number_input("Ingrese el valor del Parametro:", min_value=0, step=1)

    # Botón para actualizar el campo Faltante en la tabla Inventario
    if st.button("Actualizar Parametros"):
        if qr_code and faltante is not None:
            actualizar_faltante(qr_code, faltante)
            st.success("Faltante actualizado exitosamente")

