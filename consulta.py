
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .container {
        display: flex;
    }
    .logo-text {
        font-weight: 700 !important;
        font-size: 30px !important;
        color: black !important;
        padding-top: 50px !important;
    }
    .logo-img {
        float: right;
    }
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("estilos.css")

# Conexión a la base de datos SQLite
conn = sqlite3.connect('inventario.db')
cursor = conn.cursor()
if "user" not in st.session_state:
    st.session_state.username = ""

# Función para realizar la consulta
def consulta_entre_fechas(fecha_inicio, fecha_fin, tipo_movimiento):
    
    fecha_fin += timedelta(days=1)
    cursor.execute("""
    SELECT mi.Tipo_Movimiento, mi.Cantidad_Movida,  p.Nombre, mi.Fecha_Hora_Movimiento, mi.Razon_Movimiento
    FROM Movimiento_Inventario mi
    JOIN Productos p ON mi.Codigo = p.Codigo
    -- WHERE mi.Fecha_Hora_Movimiento BETWEEN ? AND ? AND mi.Tipo_Movimiento = ?
    WHERE mi.Fecha_Hora_Movimiento >= ? AND mi.Fecha_Hora_Movimiento <= ? AND mi.Tipo_Movimiento = ?
    """, (fecha_inicio, fecha_fin, tipo_movimiento))
    data = cursor.fetchall()
    return data

# Encabezado de la aplicación
st.title("Consulta de Stock")
#st.write("Usuario: " + str(st.session_state.user))
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)
if "ingreso" not in st.session_state:
    st.session_state.ingreso = ""

if st.session_state.ingreso == "":
    st.warning("Por favor Ingrese Correctamente")
else:
    # Formulario de consulta
    fecha_inicio = st.date_input('Fecha de inicio')
    fecha_fin = st.date_input('Fecha de fin')
    tipo_movimiento = st.selectbox('Tipo de Movimiento', ['Entrada', 'Salida'])

    if st.button('Consultar'):
        if fecha_inicio <= fecha_fin:
            data = consulta_entre_fechas(fecha_inicio, fecha_fin, tipo_movimiento)
            if len(data) > 0:
                st.write('Resultados de la consulta:')
                df = pd.DataFrame(data, columns=['Tipo_Movimiento', 'Cantidad_Movida', 'Nombre', 'Fecha_Hora_Movimiento', 'Razon_Movimiento'])
                df['Fecha_Hora_Movimiento'] = pd.to_datetime(df['Fecha_Hora_Movimiento'])
                df['Fecha_Hora_Movimiento'] = df['Fecha_Hora_Movimiento'].dt.strftime('%d/%m/%Y')  # Cambio del formato de la fecha
                st.dataframe(df)

                # Agrega esta parte para mostrar el DataFrame agrupado por "Nombre" y "Fecha_Hora_Movimiento"
                st.subheader('Productos por Fecha y Nombre')
                grouped_df = df.groupby(['Nombre', 'Fecha_Hora_Movimiento'])['Cantidad_Movida'].sum().reset_index()
                st.dataframe(grouped_df)

                fig = px.bar(df, x='Nombre', y='Cantidad_Movida', title='Cantidad movida por fecha')
                st.plotly_chart(fig)
            else:
                st.warning('No se encontraron resultados para los filtros seleccionados.')
        else:
            st.error('La fecha de inicio debe ser anterior a la fecha de fin.')

    # Cierre de la conexión a la base de datos
    conn.close()
