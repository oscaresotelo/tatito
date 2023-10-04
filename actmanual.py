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

# Función para conectar a la base de datos SQLite
def connect_db():
    conn = sqlite3.connect('inventario.db')
    return conn

# Función para buscar productos por nombre
def search_product_by_name(conn, nombre):
    query = f"SELECT * FROM Productos WHERE Nombre LIKE '%{nombre}%'"
    result = pd.read_sql(query, conn)
    return result

# Función para actualizar la cantidad y unidad de medida de un producto
def update_product(conn, codigo, cantidad, unidad_medida):
    query = f"UPDATE Productos SET Cantidad_Medida = {cantidad}, Unidad_Medida = '{unidad_medida}' WHERE Codigo = {codigo}"
    conn.execute(query)
    conn.commit()

def main():
    st.title("Gestión de Inventario")

    # Conectar a la base de datos
    conn = connect_db()

    # Barra lateral para búsqueda por nombre
    st.header("Búsqueda por Nombre")
    nombre_busqueda = st.text_input("Ingrese el nombre del producto:")

    if nombre_busqueda:
        # Realizar la búsqueda
        results = search_product_by_name(conn, nombre_busqueda)

        if not results.empty:
            st.header("Resultados de la búsqueda:")
            st.dataframe(results)

            # Seleccionar un producto para modificar
            selected_index = st.selectbox("Seleccione un producto para modificar:", results.index)
            if selected_index  >= 0:
                cantidad = st.number_input("Nueva Cantidad:", value=int(results.at[selected_index, 'Cantidad_Medida']))
                unidad_medida = st.text_input("Nueva Unidad de Medida:", value=results.at[selected_index, 'Unidad_Medida'])

                if st.button("Modificar Producto"):
                    

                    # Actualizar el producto
                    update_product(conn, results.at[selected_index, 'Codigo'], cantidad, unidad_medida)
                    st.success("Producto modificado con éxito.")


    conn.close()

if __name__ == '__main__':
    main()
