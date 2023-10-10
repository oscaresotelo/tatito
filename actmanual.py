import streamlit as st
import sqlite3
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
if "user" not in st.session_state:
    st.session_state.user = ""
    st.write("usuario incorrecto")
else:
    st.write(st.session_state.user)
if "ingreso" not in st.session_state:
    st.session_state.ingreso = ""

if st.session_state.ingreso == "":
    st.warning("Por favor Ingrese Correctamente")
st.markdown(hide_st_style, unsafe_allow_html=True)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("estilos.css")
# Conexión a la base de datos SQLite
conn = sqlite3.connect('inventario.db')
cursor = conn.cursor()

# Función para buscar productos por nombre
def buscar_productos_por_nombre(nombre):
    cursor.execute("SELECT Codigo, Nombre FROM Productos WHERE Nombre LIKE ?", ('%' + nombre + '%',))
    return cursor.fetchall()

# Función para actualizar la cantidad de stock
def actualizar_cantidad_stock(codigo, nueva_cantidad):
    cursor.execute("UPDATE Inventario SET Cantidad_Stock = ? WHERE Codigo = ?", (nueva_cantidad, codigo))
    conn.commit()

# Configuración de la aplicación Streamlit
st.title("Actualizar Cantidad de Stock")

# Formulario para buscar productos
nombre_producto = st.text_input("Ingrese el nombre del producto:")
if nombre_producto:
    productos_encontrados = buscar_productos_por_nombre(nombre_producto)
    if productos_encontrados:
        st.write("Productos encontrados:")
        for producto in productos_encontrados:
            st.write(f"Código: {producto[0]}, Nombre: {producto[1]}")

        # Selección del producto a actualizar
        producto_seleccionado = st.selectbox("Seleccione un producto para actualizar:", [str(producto[0]) for producto in productos_encontrados])
        
        # Formulario para actualizar la cantidad de stock
        nueva_cantidad = st.number_input("Nueva cantidad de stock:")
        if st.button("Actualizar Cantidad de Stock"):
            if producto_seleccionado:
                actualizar_cantidad_stock(producto_seleccionado, nueva_cantidad)
                st.success("Cantidad de stock actualizada con éxito.")

# Cerrar la conexión a la base de datos al finalizar
conn.close()
