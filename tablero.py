
import streamlit as st
import sqlite3
import pandas as pd
import io
import base64

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

def highlight_red(val):
    return f'color: red'

def highlight_blue(val):
    return f'color: blue'

# Configurar la aplicación de Streamlit

# Conexión a la base de datos SQLite
conn = sqlite3.connect('inventario.db')
cursor = conn.cursor()
# if "user" not in st.session_state:
# 	st.session_state = ""

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

    # Agregar una función para exportar los datos a un archivo Excel
    def export_to_excel(df, condition):
        if condition == "Faltante":
            filename = "productos_faltantes.xlsx"
        elif condition == "Stockeado":
            filename = "productos_stockeados.xlsx"
        else:
            return None

        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')

        return buffer.getvalue()

    # Función para crear un enlace de descarga para el archivo
    def get_binary_file_downloader_html(bin_data, file_label='File'):
        b64 = base64.b64encode(bin_data).decode()
        custom_css = f""" 
            <style>
                .download-link {{
                    background-color: #008CBA;
                    color: #FFFFFF;
                    padding: 8px 12px;
                    border-radius: 4px;
                    text-decoration: none;
                    font-weight: bold;
                    display: inline-block;
                    margin-top: 10px;
                }}
                .download-link:hover {{
                    background-color: #005f7f;
                }}
            </style>
        """
        dl_link = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_label}.xlsx" class="download-link">{file_label}</a>'
        return f"{custom_css}{dl_link}"

    # Crear la aplicación Streamlit
    def main():
        
        #usuario = st.write("Usuario: " + str(st.session_state.user))
        # st.markdown("<h1 style='text-align: center'>Tablero de Control</h1>", unsafe_allow_html=True)
        st.title("Tablero de Control")
        st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

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

        # Exportar a Excel
        if st.button("Descargar Excel"):
            buffer = export_to_excel(df, condicion)
            if condicion == "Faltante":
                filename = "productos_faltantes"
            elif condicion == "Stockeado":   
            	filename = "productos_stockeados"
            else:
            	filename = "archivo"
            st.success(f"Archivo Excel generado con éxito.")
            st.markdown(get_binary_file_downloader_html(buffer, filename), unsafe_allow_html=True)
        # Cerrar la conexión a la base de datos al finalizar
        conn.close()

    if __name__ == '__main__':
        main()
