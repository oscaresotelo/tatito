import streamlit as st
import pandas as pd
import sqlite3
import pygwalker as pyg

# Set page configuration
st.set_page_config(
    page_title="Tablero ",
    page_icon=":snake:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Connect to SQLite database
conn = sqlite3.connect("inventario.db")
cursor = conn.cursor()

# Load Data from the SQLite database with JOIN between Inventario and Productos
@st.cache(allow_output_mutation=True)
def load_data():
    query = """
    SELECT
        I.ID_Inventario,
        I.Codigo AS Codigo_Inventario,
        I.Cantidad_Stock,
        I.Ubicacion_Almacen,
        I.Fecha_Actualizacion,
        I.Faltante,
        I.FechaVto,
        P.ID_Producto,
        P.Codigo AS Codigo_Producto,
        P.Nombre,
        P.Rubro,
        P.Subrubro,
        P.Categoria,
        P.Descripcion,
        P.Precio_Compra,
        P.Precio_Venta,
        P.Proveedor,
        P.Unidad_Medida,
        P.ID_Producto_Nuevo
    FROM Inventario I
    INNER JOIN Productos P ON I.Codigo = P.Codigo
    """
    df = pd.read_sql(query, conn)
    return df

df = load_data()

# Set title and subtitle
st.title('Tablero de Visualización')
st.subheader('Datos de Inventario y Productos')

# Display PyGWalker
def load_config(file_path):
    with open(file_path, 'r') as config_file:
        config_str = config_file.read()
    return config_str

# config = load_config('config.json')
pyg.walk(df, env='Streamlit', dark='dark')

# Close the SQLite connection when done
conn.close()
