import streamlit as st
import sqlite3
import pandas as pd

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


# Conexión a la base de datos SQLite
conn = sqlite3.connect('inventario.db')
cursor = conn.cursor()

# Función para realizar la consulta
def consulta_entre_fechas(fecha_inicio, fecha_fin, tipo_movimiento):
    cursor.execute("""
    SELECT mi.Tipo_Movimiento, mi.Cantidad_Movida,  p.Nombre, mi.Fecha_Hora_Movimiento, mi.Razon_Movimiento
    FROM Movimientos_Inventario mi
    JOIN Productos p ON mi.Codigo = p.Codigo
    WHERE mi.Fecha_Hora_Movimiento BETWEEN ? AND ? AND mi.Tipo_Movimiento = ?
    """, (fecha_inicio, fecha_fin, tipo_movimiento))
    data = cursor.fetchall()
    return data

# Encabezado de la aplicación
st.markdown("<h1 style='text-align: center; color: red;'>Consulta de Stock</h1>", unsafe_allow_html=True)

# Formulario de consulta
st.sidebar.header('Filtros')
fecha_inicio = st.sidebar.date_input('Fecha de inicio')
fecha_fin = st.sidebar.date_input('Fecha de fin')
tipo_movimiento = st.sidebar.selectbox('Tipo de Movimiento', ['Entrada', 'Salida'])

if st.sidebar.button('Consultar'):
    if fecha_inicio <= fecha_fin:
        data = consulta_entre_fechas(fecha_inicio, fecha_fin, tipo_movimiento)
        if len(data) > 0:
            st.write('Resultados de la consulta:')
            df = pd.DataFrame(data, columns=['Tipo_Movimiento', 'Cantidad_Movida', 'Nombre','Fecha_Hora_Movimiento', 'Razon_Movimiento'])
            st.write(df)
        else:
            st.warning('No se encontraron resultados para los filtros seleccionados.')
    else:
        st.error('La fecha de inicio debe ser anterior a la fecha de fin.')

# Cierre de la conexión a la base de datos
conn.close()
