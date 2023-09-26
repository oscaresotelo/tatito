
# import streamlit as st
# import sqlite3
# import pandas as pd


# hide_st_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             header {visibility: hidden;}
#                      .container {
#                 display: flex;
#             }
#             .logo-text {
#                 font-weight:700 !important;
#                 font-size:30px !important;
#                 color: black !important;
#                 padding-top: 50px !important;
#             }
#             .logo-img {
#                 float:right;
#             }
#             </style>
#             """
# st.markdown(hide_st_style, 

#     unsafe_allow_html=True)

# def local_css(file_name):
#     with open(file_name) as f:
#         st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
# local_css("estilos.css")

# def highlight_red(val):
#     return f'color: red'
# # Configurar la aplicación de Streamlit


# # Conexión a la base de datos SQLite
# conn = sqlite3.connect('inventario.db')
# cursor = conn.cursor()
# if "ingreso" not in st.session_state:
#       st.session_state.ingreso = ""


# if st.session_state.ingreso == "":
#     st.warning("Por favor Ingrese Correctamente")
# else:
# 	# Crear una función para obtener los registros de Inventario relacionados con Productos
# 	def obtener_registros():
# 	    cursor.execute("""
# 	    SELECT  Inventario.Cantidad_Stock
# 	           , Inventario.Faltante, Productos.Nombre , Inventario.Fecha_Actualizacion
# 	    FROM Inventario
# 	    INNER JOIN Productos ON Inventario.Codigo = Productos.Codigo
# 	    WHERE Inventario.Faltante >= Inventario.Cantidad_Stock
# 	    """)
# 	    return cursor.fetchall()

# 	# Crear la aplicación Streamlit
# 	def main():
# 	    st.markdown("<h1 style='text-align: center'>Tablero de Control</h1>", unsafe_allow_html=True)
	    
# 	    registros = obtener_registros()
	    
# 	    if not registros:
# 	        st.warning('No se encontraron registros.')
# 	    else:
# 	        st.write('Registros de Productos en Falta:')
	        
# 	        # Mapear los nombres de las columnas
# 	        column_names = ["Stock", "Mínimo", "Nombre", "Última Fecha"]
	        
# 	        # Crear un DataFrame de pandas para los registros
# 	        df = pd.DataFrame(registros, columns=column_names)
	        
	       
# 	        # Mostrar el DataFrame con estilo
	        
# 	        st.dataframe(df.style.applymap(highlight_red, subset=['Stock']))
# 	    # Cerrar la conexión a la base de datos al finalizar
# 	    conn.close()

# 	if __name__ == '__main__':
# 	    main()

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
st.markdown(hide_st_style, unsafe_allow_html=True)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("estilos.css")

def highlight_red(val):
    return f'color: red'

def highlight_blue(val):
    return f'color: blue'

# Configurar la aplicación de Streamlit

# Conexión a la base de datos SQLite
conn = sqlite3.connect('inventario.db')
cursor = conn.cursor()

if "ingreso" not in st.session_state:
    st.session_state.ingreso = ""

if st.session_state.ingreso == "":
    st.warning("Por favor Ingrese Correctamente")
else:
    # Crear una función para obtener los registros de Inventario relacionados con Productos
    def obtener_registros(condicion):
        if condicion == "Faltante":
            cursor.execute("""
                SELECT Inventario.Cantidad_Stock, Inventario.Faltante, Productos.Nombre, Inventario.Fecha_Actualizacion
                FROM Inventario
                INNER JOIN Productos ON Inventario.Codigo = Productos.Codigo
                WHERE Inventario.Faltante >= Inventario.Cantidad_Stock
            """)
        elif condicion == "Stockeado":
            cursor.execute("""
                SELECT Inventario.Cantidad_Stock, Inventario.Faltante, Productos.Nombre, Inventario.Fecha_Actualizacion
                FROM Inventario
                INNER JOIN Productos ON Inventario.Codigo = Productos.Codigo
                WHERE Inventario.Faltante <= Inventario.Cantidad_Stock
            """)


        else:
            st.error("Error inesperado")

        return cursor.fetchall()

    # Crear la aplicación Streamlit
    def main():
        # st.markdown("<h1 style='text-align: center'>Tablero de Control</h1>", unsafe_allow_html=True)
        st.title("Tablero de Control")
        st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

        # Agregar un control para seleccionar la condición
        condicion = st.radio("Selecciona una condición:", ["Stockeado", "Faltante"])
        if condicion == "Stockeado":

	        registros = obtener_registros(condicion)

	        if not registros:
	            st.warning('No se encontraron registros.')
	        else:
	            st.write('Registros de Productos en Falta:')

	            # Mapear los nombres de las columnas
	            column_names = ["Stock", "Mínimo", "Nombre", "Última Fecha"]

	            # Crear un DataFrame de pandas para los registros
	            df = pd.DataFrame(registros, columns=column_names)

	            # Mostrar el DataFrame con estilo
	            st.dataframe(df.style.applymap(highlight_blue, subset=['Stock']))

	        # Cerrar la conexión a la base de datos al finalizar
	        conn.close()

        else:
            registros = obtener_registros(condicion)

            if not registros:
                st.warning('No se encontraron registros.')
            else:
                st.write('Registros de Productos en Falta:')

	            # Mapear los nombres de las columnas
                column_names = ["Stock", "Mínimo", "Nombre", "Última Fecha"]

	            # Crear un DataFrame de pandas para los registros
                df = pd.DataFrame(registros, columns=column_names)

	            # Mostrar el DataFrame con estilo
                st.dataframe(df.style.applymap(highlight_red, subset=['Stock']))

	        # Cerrar la conexión a la base de datos al finalizar
            conn.close()	

    if __name__ == '__main__':
        main()
