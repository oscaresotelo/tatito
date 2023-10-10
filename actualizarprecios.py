# import sqlite3
# import csv

# # Conexión a la base de datos SQLite
# conexion = sqlite3.connect('inventario.db')
# cursor = conexion.cursor()

# # Nombre del archivo CSV
# archivo_csv = 'tatito.csv'

# try:
#     # Abrir el archivo CSV y leer los datos
#     with open(archivo_csv, 'r', newline='', encoding='utf-8') as archivo:
#         lector_csv = csv.DictReader(archivo, delimiter=';')
        
#         for fila in lector_csv:
#             nombre_producto_csv = fila['Nombre']
#             precio_venta_csv = fila['Precio_Venta'].replace('.', '').replace(',', '.')
            
#             # Consulta para actualizar el Precio_Venta en la tabla Productos
#             cursor.execute(
#                 "UPDATE Productos SET Precio_Venta = ? WHERE Nombre = ?",
#                 (precio_venta_csv, nombre_producto_csv)
#             )

#     # Guardar los cambios en la base de datos
#     conexion.commit()
#     print("Actualización completada correctamente.")
    
# except Exception as e:
#     conexion.rollback()  # En caso de error, deshacer cualquier cambio pendiente en la base de datos
#     print(f"Error: {str(e)}")

# finally:
#     # Cerrar la conexión con la base de datos
#     conexion.close()
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
    cursor.execute("SELECT Codigo, Nombre, Precio_Venta, Precio_Compra FROM Productos WHERE Nombre LIKE ?", ('%' + nombre + '%',))
    return cursor.fetchall()

# Función para actualizar el precio de venta y precio de compra
def actualizar_precios(codigo, nuevo_precio_venta, nuevo_precio_compra):
    cursor.execute("UPDATE Productos SET Precio_Venta = ?, Precio_Compra = ? WHERE Codigo = ?", (nuevo_precio_venta, nuevo_precio_compra, codigo))
    conn.commit()

# Configuración de la aplicación Streamlit
st.title("Actualizar Precios de Productos")

# Formulario para buscar productos
nombre_producto = st.text_input("Ingrese el nombre del producto:")
if nombre_producto:
    productos_encontrados = buscar_productos_por_nombre(nombre_producto)
    if productos_encontrados:
        st.write("Productos encontrados:")
        for producto in productos_encontrados:
            st.write(f"Código: {producto[0]}, Nombre: {producto[1]}, Precio Venta: {producto[2]}, Precio Compra: {producto[3]}")

        # Selección del producto a actualizar
        producto_seleccionado = st.selectbox("Seleccione un producto para actualizar:", [str(producto[0]) for producto in productos_encontrados])

        # Formulario para actualizar el precio de venta y precio de compra
        nuevo_precio_venta = st.number_input("Nuevo precio de venta:")
        nuevo_precio_compra = st.number_input("Nuevo precio de compra:")
        if st.button("Actualizar Precios"):
            if producto_seleccionado:
                actualizar_precios(producto_seleccionado, nuevo_precio_venta, nuevo_precio_compra)
                st.success("Precios actualizados con éxito.")

# Cerrar la conexión a la base de datos al finalizar
conn.close()
