
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
if "ingreso" not in st.session_state:
      st.session_state.ingreso = ""


if st.session_state.ingreso == "":
    st.warning("Por favor Ingrese Correctamente")
else:
	# Crear una función para obtener los registros de Inventario relacionados con Productos
	def obtener_registros():
	    cursor.execute("""
	    SELECT  Inventario.Cantidad_Stock, 
	           Inventario.Fecha_Actualizacion, Inventario.Faltante, Productos.Nombre
	    FROM Inventario
	    INNER JOIN Productos ON Inventario.Codigo = Productos.Codigo
	    WHERE Inventario.Faltante >= Inventario.Cantidad_Stock
	    """)
	    return cursor.fetchall()

	# Crear la aplicación Streamlit
	def main():
	    st.markdown("<h1 style='text-align: center; color: red;'>Tablero de Control</h1>", unsafe_allow_html=True)
	    
	    registros = obtener_registros()
	    
	    if not registros:
	        st.warning('No se encontraron registros.')
	    else:
	        st.write('Registros de Productos en Falta:')
	        
	        # Mapear los nombres de las columnas
	        column_names = ["Stock", "Última Fecha", "Mínimo", "Nombre"]
	        
	        # Crear un DataFrame de pandas para los registros
	        df = pd.DataFrame(registros, columns=column_names)
	        
	        # Crear una columna adicional para la columna "Stock" resaltada en rojo
	        df['Stock Resaltado'] = df['Stock'].apply(lambda x: f'color: red' if x == df['Stock'].min() else '')
	        
	        # Mostrar el DataFrame con estilo
	        st.dataframe(df.style.applymap(lambda x: x, subset=['Stock Resaltado']))

	    # Cerrar la conexión a la base de datos al finalizar
	    conn.close()

	if __name__ == '__main__':
	    main()

