
import streamlit as st
import sqlite3

from streamlit_qrcode_scanner import qrcode_scanner
# Conexión a la base de datos SQLite
conn = sqlite3.connect('inventario.db')
cursor = conn.cursor()


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
# Función para buscar y mostrar los datos del producto por el campo "Codigo"
def buscar_producto(codigo):
    cursor.execute("SELECT * FROM Productos WHERE Codigo = ?", (codigo,))
    producto = cursor.fetchone()
    return producto

# Función para actualizar los datos del producto por el campo "Codigo"
def actualizar_producto(codigo, nombre, rubro, subrubro, categoria, descripcion, precio_compra, precio_venta, proveedor, unidad_medida, id_producto_nuevo, cantidad_medida):
    cursor.execute("UPDATE Productos SET Nombre=?, Rubro=?, Subrubro=?, Categoria=?, Descripcion=?, Precio_Compra=?, Precio_Venta=?, Proveedor=?, Unidad_Medida=?, ID_Producto_Nuevo=?, Cantidad_Medida=? WHERE Codigo=?", (nombre, rubro, subrubro, categoria, descripcion, precio_compra, precio_venta, proveedor, unidad_medida, id_producto_nuevo, cantidad_medida, codigo))
    conn.commit()

st.title('Actualización de Productos')
if "ingreso" not in st.session_state:
    st.session_state.ingreso = ""

if st.session_state.ingreso == "":
    st.warning("Por favor Ingrese Correctamente")
else:
    qr_code = qrcode_scanner()

    if qr_code:
        producto = buscar_producto(qr_code)
        if producto:
            st.subheader('Datos del Producto:')
            st.write(f'ID_Producto: {producto[0]}')
            st.write(f'Código: {producto[1]}')
            nombre = st.text_input('Nombre:', producto[2])
            rubro = st.text_input('Rubro:', producto[3])
            subrubro = st.text_input('Subrubro:', producto[4])
            categoria = st.text_input('Categoría:', producto[5])
            descripcion = st.text_area('Descripción:', producto[6])
            preciocompra  = st.number_input('Precio de Compra:', value=producto[7])
            precioventa = st.number_input('Precio de Venta:', value=producto[8])
            proveedor = st.text_input('Proveedor:', producto[9])
            unidadmedida = st.text_input('Unidad de Medida:', producto[10])
            idproducto = st.text_input('ID Producto Nuevo:', producto[11])
            cantidadmedida = st.text_input('Cantidad Por Medida:', producto[12])
                
            if st.button('Actualizar'):
                actualizar_producto(producto[1], nombre, rubro, subrubro, categoria, descripcion, preciocompra, precioventa, proveedor, unidadmedida, idproducto, cantidadmedida)
                st.success('Producto actualizado con éxito.')

    # Cierre de la conexión a la base de datos
    conn.close()
