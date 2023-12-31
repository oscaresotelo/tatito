import streamlit as st
import sqlite3
from streamlit_qrcode_scanner import qrcode_scanner
import datetime



if "user" not in st.session_state:
    st.session_state.user = ""
    st.write("Sin Usuario")
else:
    st.write("Usuario: " + str(st.session_state.user))

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

st.markdown("<h1 style='text-align: center; color: red;'>Registro de Movimientos de Inventario</h1>", unsafe_allow_html=True)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
local_css("estilos.css")


# Función para buscar en la base de datos
if "ingreso" not in st.session_state:
    st.session_state.ingreso = ""

if st.session_state.ingreso == "":
    st.warning("Por favor Ingrese Correctamente")

else:
    def buscar_producto_por_codigo(codigo):
        conn = sqlite3.connect("inventario.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.Nombre,  p.Precio_Venta, p.Precio_Compra
            FROM Productos p
            
            WHERE p.Codigo=?
        """, (codigo,))
        producto = cursor.fetchone()
        conn.close()
        return producto

    def agregar_producto(codigo, nombre, descripcion, precio_compra, precio_venta, proveedor, unidad_medida,cantidad_medida):
        conn = sqlite3.connect("inventario.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Productos (Codigo, Nombre,  Descripcion, Precio_Compra, Precio_Venta, Proveedor, Unidad_Medida, Cantidad_Medida)
            VALUES (?, ?, ?, ?, ?, ?,?,?)
        """, (codigo, nombre,  descripcion, precio_compra, precio_venta, proveedor, unidad_medida,cantidad_medida))
        conn.commit()
        conn.close()

    
    def agregar_movimiento_inventario(codigo, tipo_movimiento, cantidad_movida, ubicacion_almacen, razon_movimiento, fechavto):
        if tipo_movimiento == "Entrada":
            conn = sqlite3.connect("inventario.db")
            cursor = conn.cursor()
            fecha_hora_movimiento = datetime.datetime.now()

            # Obtener el valor de Cantidad_Medida de la tabla "Productos" usando el código
            cursor.execute("SELECT Cantidad_Medida FROM Productos WHERE Codigo=?", (codigo,))
            cantidad_medida_producto = cursor.fetchone()[0]


            # Calcular la cantidad movida multiplicando por Cantidad_Medida
            cantidad_movida_total = cantidad_movida * cantidad_medida_producto

            cursor.execute("""
                INSERT INTO Movimiento_Inventario (Codigo, Tipo_Movimiento, Cantidad_Movida, Fecha_Hora_Movimiento, usuario, Razon_Movimiento,FechaVto)
                VALUES (?, ?, ?, ?, ?, ?,?)
            """, (codigo, tipo_movimiento, cantidad_movida_total, fecha_hora_movimiento, usuario, razon_movimiento,fechavto))
            conn.commit()
            conn.close()

            # Actualizar la tabla "Inventario"
            conn_inventario = sqlite3.connect("inventario.db")
            cursor_inventario = conn_inventario.cursor()

            # Buscar el código en la tabla "Inventario"
            cursor_inventario.execute("SELECT * FROM Inventario WHERE Codigo=?", (codigo,))
            row = cursor_inventario.fetchone()

            if row is None:
                # Si no existe el código, insertarlo en la tabla "Inventario"
                cursor_inventario.execute("INSERT INTO Inventario (Codigo, Cantidad_Stock, Fecha_Actualizacion) VALUES (?, ?, ?)", (codigo, 0, datetime.datetime.now()))
                conn_inventario.commit()

            # Sumar al campo Cantidad_Stock si el Tipo_Movimiento es "Entrada"
            if tipo_movimiento == "Entrada":
                cursor_inventario.execute("UPDATE Inventario SET Cantidad_Stock = Cantidad_Stock + ?, Fecha_Actualizacion = ? WHERE Codigo = ?", (cantidad_movida_total, datetime.datetime.now(), codigo))
                conn_inventario.commit()
            

            conn_inventario.close()
        else:
            conn = sqlite3.connect("inventario.db")
            cursor = conn.cursor()
            fecha_hora_movimiento = datetime.datetime.now()
            cursor.execute("""
                INSERT INTO Movimiento_Inventario (Codigo, Tipo_Movimiento, Cantidad_Movida, Fecha_Hora_Movimiento, usuario, Razon_Movimiento,FechaVto)
                VALUES (?, ?, ?, ?, ?, ?,?)
            """, (codigo, tipo_movimiento, cantidad_movida, fecha_hora_movimiento, usuario, razon_movimiento,fechavto))
            conn.commit()
            conn.close()

            # Actualizar la tabla "Inventario"
            conn_inventario = sqlite3.connect("inventario.db")
            cursor_inventario = conn_inventario.cursor()

            # Buscar el código en la tabla "Inventario"
            cursor_inventario.execute("SELECT * FROM Inventario WHERE Codigo=?", (codigo,))
            row = cursor_inventario.fetchone()

            if row is None:
                # Si no existe el código, insertarlo en la tabla "Inventario"
                cursor_inventario.execute("INSERT INTO Inventario (Codigo, Cantidad_Stock, Fecha_Actualizacion) VALUES (?, ?, ?)", (codigo, 0, datetime.datetime.now()))
                conn_inventario.commit()

            # Sumar al campo Cantidad_Stock si el Tipo_Movimiento es "Entrada"
            # if tipo_movimiento == "Entrada":
            #     cursor_inventario.execute("UPDATE Inventario SET Cantidad_Stock = Cantidad_Stock + ?, Fecha_Actualizacion = ? WHERE Codigo = ?", (cantidad_movida, datetime.datetime.now(), codigo))
            #     conn_inventario.commit()
            if tipo_movimiento == "Salida":
                cursor_inventario.execute("UPDATE Inventario SET Cantidad_Stock = Cantidad_Stock - ?, Fecha_Actualizacion = ? WHERE Codigo = ?", (cantidad_movida, datetime.datetime.now(), codigo))
                conn_inventario.commit()

            conn_inventario.close()

    qr_code = qrcode_scanner(key='qrcode_scanner')

    if qr_code:
        producto = buscar_producto_por_codigo(qr_code)
        if producto:
            st.write(qr_code)
            st.write("Datos del producto:")
            st.write(f"Nombre: {producto[0]}")
            st.write(f"Precio Venta: {producto[1]}")
            #st.write(f"Precio Costo: {producto[2]}")

            # Formulario para agregar movimiento de inventario
            st.write("Agregar movimiento de inventario:")
            tipo_movimiento = st.selectbox("Tipo de Movimiento", ["Entrada", "Salida"])
            cantidad_movida = st.number_input("Cantidad Movida:", min_value=1)
            usuario = st.text_input("usuario:")
            razon_movimiento = st.text_area("Ubicacion Mercaderia:")
            fecha_vencimiento = st.date_input("Ingrese Fecha Vencimiento")
            if st.button("Guardar Movimiento"):
                agregar_movimiento_inventario(qr_code, tipo_movimiento, cantidad_movida, usuario, razon_movimiento,fecha_vencimiento)
                st.success("Movimiento de inventario registrado correctamente.")

        else:
            st.write(f"Producto con código {qr_code} no encontrado en la base de datos.")
            st.write("Agregar nuevo producto:")
            st.write("Luego, leer Nuevamente Para Cargar Movimiento")
            nuevo_nombre = st.text_input("Nombre:")
            # nuevo_rubro = st.text_input("Rubro:")
            # nuevo_subrubro = st.text_input("Subrubro:")
            # nueva_categoria = st.text_input("Categoria:")
            nueva_descripcion = st.text_area("Descripción:")
            nuevo_precio_compra = st.number_input("Precio de Compra:")
            nuevo_precio_venta = st.number_input("Precio de Venta:")
            nuevo_proveedor = st.text_input("Proveedor:")
            nueva_unidad_medida = st.text_input("Unidad de Medida:")
            nueva_cantidad_medida = st.number_input("Ingresar Cantidad")
            #fecha_vencimiento = st.date_input("Ingrese Fecha Vencimiento")
            
            if st.button("Guardar Producto"):
                agregar_producto(qr_code, nuevo_nombre,  nueva_descripcion, nuevo_precio_compra, nuevo_precio_venta, nuevo_proveedor, nueva_unidad_medida,nueva_cantidad_medida)
                st.success(f"Producto con código {qr_code} agregado correctamente.")
    else:
        st.write("Escanea un código QR para buscar un producto.")
