
import streamlit as st
import sqlite3
from streamlit_qrcode_scanner import qrcode_scanner
import datetime

st.markdown("<h1 style='text-align: center; color: red;'>Registro de Movimientos de Inventario</h1>", unsafe_allow_html=True)
# Función para buscar en la base de datos
def buscar_producto_por_codigo(codigo):
    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.Nombre, r.NombreRubro, p.Precio_Venta
        FROM Productos p
        INNER JOIN Rubros r ON p.Rubro = r.CodRubro
        WHERE p.Codigo=?
    """, (codigo,))
    producto = cursor.fetchone()
    conn.close()
    return producto

def agregar_producto(codigo, nombre, rubro, subrubro, categoria, descripcion, precio_compra, precio_venta, proveedor, unidad_medida):
    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Productos (Codigo, Nombre, Rubro, Subrubro, Categoria, Descripcion, Precio_Compra, Precio_Venta, Proveedor, Unidad_Medida)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (codigo, nombre, rubro, subrubro, categoria, descripcion, precio_compra, precio_venta, proveedor, unidad_medida))
    conn.commit()
    conn.close()

def agregar_movimiento_inventario(codigo, tipo_movimiento, cantidad_movida, usuario, razon_movimiento):
    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()
    fecha_hora_movimiento = datetime.datetime.now()
    cursor.execute("""
        INSERT INTO Movimientos_Inventario (Codigo, Tipo_Movimiento, Cantidad_Movida, Fecha_Hora_Movimiento, Usuario, Razon_Movimiento)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (codigo, tipo_movimiento, cantidad_movida, fecha_hora_movimiento, usuario, razon_movimiento))
    conn.commit()
    conn.close()

qr_code = qrcode_scanner(key='qrcode_scanner')

if qr_code:
    producto = buscar_producto_por_codigo(qr_code)
    if producto:
        st.write(qr_code)
        st.write("Datos del producto:")
        st.write(f"Nombre: {producto[0]}")
        st.write(f"Rubro: {producto[1]}")
        st.write(f"Precio: {producto[2]}")

        # Formulario para agregar movimiento de inventario
        st.write("Agregar movimiento de inventario:")
        tipo_movimiento = st.selectbox("Tipo de Movimiento", ["Entrada", "Salida"])
        cantidad_movida = st.number_input("Cantidad Movida:", min_value=1)
        usuario = st.text_input("Usuario:")
        razon_movimiento = st.text_area("Razón del Movimiento:")
        
        if st.button("Guardar Movimiento"):
            agregar_movimiento_inventario(qr_code, tipo_movimiento, cantidad_movida, usuario, razon_movimiento)
            st.success("Movimiento de inventario registrado correctamente.")

    else:
        st.write(f"Producto con código {qr_code} no encontrado en la base de datos.")
        st.write("Agregar nuevo producto:")
        nuevo_nombre = st.text_input("Nombre:")
        nuevo_rubro = st.text_input("Rubro:")
        nuevo_subrubro = st.text_input("Subrubro:")
        nueva_categoria = st.text_input("Categoria:")
        nueva_descripcion = st.text_area("Descripción:")
        nuevo_precio_compra = st.number_input("Precio de Compra:")
        nuevo_precio_venta = st.number_input("Precio de Venta:")
        nuevo_proveedor = st.text_input("Proveedor:")
        nueva_unidad_medida = st.text_input("Unidad de Medida:")
        
        if st.button("Guardar Producto"):
            agregar_producto(qr_code, nuevo_nombre, nuevo_rubro, nuevo_subrubro, nueva_categoria, nueva_descripcion, nuevo_precio_compra, nuevo_precio_venta, nuevo_proveedor, nueva_unidad_medida)
            st.success(f"Producto con código {qr_code} agregado correctamente.")
else:
    st.write("Escanea un código QR para buscar un producto.")
