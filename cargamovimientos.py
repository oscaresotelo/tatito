# import streamlit as st
# import sqlite3
# from datetime import datetime

# # Conexión a la base de datos SQLite
# conn = sqlite3.connect('inventario.db')
# cursor = conn.cursor()

# # Crear la tabla Movimientos_inventario si no existe
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS Movimientos_inventario (
#         ID_Movimiento INTEGER PRIMARY KEY,
#         ID_Producto INTEGER,
#         Tipo_Movimiento TEXT,
#         Cantidad_Movida INTEGER,
#         Fecha_Hora_Movimiento DATETIME,
#         Usuario TEXT,
#         Razon_Movimiento TEXT,
#         FOREIGN KEY (ID_Producto) REFERENCES Productos (ID_Producto)
#     )
# ''')
# conn.commit()

# # Interfaz de usuario de Streamlit
# st.title('Registro de Movimientos de Inventario')

# # Formulario para ingresar datos de movimiento
# st.write('### Ingrese los datos del movimiento:')
# cursor.execute("SELECT ID_Producto, Nombre FROM Productos")
# productos = cursor.fetchall()
# producto_dict = {row[0]: row[1] for row in productos}
# id_productos = st.multiselect('Nombre del Producto', list(producto_dict.values()))
# tipo_movimiento = st.selectbox('Tipo de Movimiento', ['SALIDA', 'ENTRADA'])
# cantidad_movida = st.number_input('Cantidad Movida', min_value=1)
# fecha_movimiento = st.date_input('Fecha del Movimiento', value=datetime.now().date())
# hora_movimiento = st.time_input('Hora del Movimiento', value=datetime.now().time())
# usuario = st.text_input('Usuario')
# razon_movimiento = st.text_input('Razón del Movimiento')

# # Combina la fecha y la hora en un objeto datetime
# fecha_hora_movimiento = datetime.combine(fecha_movimiento, hora_movimiento)

# # Botón para agregar el movimiento
# if st.button('Agregar Movimiento'):
#     try:
#         for id_producto_seleccionado in id_productos:
#             id_producto = next((k for k, v in producto_dict.items() if v == id_producto_seleccionado), None)
#             if id_producto is not None:
#                 cursor.execute('''
#                     INSERT INTO Movimientos_inventario (ID_Producto, Tipo_Movimiento, Cantidad_Movida, Fecha_Hora_Movimiento, Usuario, Razon_Movimiento)
#                     VALUES (?, ?, ?, ?, ?, ?)
#                 ''', (id_producto, tipo_movimiento, cantidad_movida, fecha_hora_movimiento, usuario, razon_movimiento))
#                 conn.commit()
#                 st.success('Movimiento agregado correctamente.')
#             else:
#                 st.error(f'El producto seleccionado "{id_producto_seleccionado}" no existe.')
#     except sqlite3.Error as e:
#         st.error(f'Error al agregar el movimiento: {e}')

# # Mostrar los datos de la tabla Movimientos_inventario con la descripción del producto
# st.write('### Movimientos de Inventario:')
# cursor.execute('''
#     SELECT MI.ID_Movimiento, P.Nombre, MI.Tipo_Movimiento, MI.Cantidad_Movida, MI.Fecha_Hora_Movimiento, MI.Usuario, MI.Razon_Movimiento
#     FROM Movimientos_inventario MI
#     JOIN Productos P ON MI.ID_Producto = P.ID_Producto
# ''')
# movimientos = cursor.fetchall()

# if movimientos:
#     st.table(movimientos)
# else:
#     st.info('No hay movimientos registrados.')

# # Cerrar la conexión a la base de datos
# conn.close()
import streamlit as st
import sqlite3
from datetime import datetime

# Conexión a la base de datos SQLite
conn = sqlite3.connect('inventario.db')
cursor = conn.cursor()

# Crear la tabla Movimientos_inventario si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Movimientos_inventario (
        ID_Movimiento INTEGER PRIMARY KEY,
        ID_Producto INTEGER,
        Tipo_Movimiento TEXT,
        Cantidad_Movida INTEGER,
        Fecha_Hora_Movimiento DATETIME,
        Usuario TEXT,
        Razon_Movimiento TEXT,
        FOREIGN KEY (ID_Producto) REFERENCES Productos (ID_Producto)
    )
''')

# Crear la tabla Inventario si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Inventario (
        ID_Producto INTEGER PRIMARY KEY,
        Cantidad_Stock INTEGER,
        FOREIGN KEY (ID_Producto) REFERENCES Productos (ID_Producto)
    )
''')

conn.commit()

# Interfaz de usuario de Streamlit
# st.title('Registro de Movimientos de Inventario')
st.markdown("<h1 style='text-align: center; color: red;'>Registro de Movimientos de Inventario</h1>", unsafe_allow_html=True)
# Formulario para ingresar datos de movimiento
st.write('### Ingrese los datos del movimiento:')
cursor.execute("SELECT Codigo, Nombre FROM Productos")
productos = cursor.fetchall()
producto_dict = {row[0]: row[1] for row in productos}
id_productos = st.multiselect('Nombre del Producto', list(producto_dict.values()))
tipo_movimiento = st.selectbox('Tipo de Movimiento', ['SALIDA', 'ENTRADA'])
cantidad_movida = st.number_input('Cantidad Movida', min_value=1)
fecha_movimiento = st.date_input('Fecha del Movimiento', value=datetime.now().date())
hora_movimiento = st.time_input('Hora del Movimiento', value=datetime.now().time())
usuario = st.text_input('Usuario')
razon_movimiento = st.text_input('Razón del Movimiento')

# Combina la fecha y la hora en un objeto datetime
fecha_hora_movimiento = datetime.combine(fecha_movimiento, hora_movimiento)

# Botón para agregar el movimiento
if st.button('Agregar Movimiento'):
    try:
        for id_producto_seleccionado in id_productos:
            id_producto = next((k for k, v in producto_dict.items() if v == id_producto_seleccionado), None)
            if id_producto is not None:
                cursor.execute('''
                    INSERT INTO Movimientos_inventario (Codigo, Tipo_Movimiento, Cantidad_Movida, Fecha_Hora_Movimiento, Usuario, Razon_Movimiento)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (Codigo, tipo_movimiento, cantidad_movida, fecha_hora_movimiento, usuario, razon_movimiento))
                
                # Actualizar el inventario
                if tipo_movimiento == 'ENTRADA':
                    cursor.execute('''
                        UPDATE Inventario
                        SET Cantidad_Stock = Cantidad_Stock + ?
                        WHERE Codigo = ?
                    ''', (cantidad_movida, id_producto))
                elif tipo_movimiento == 'SALIDA':
                    cursor.execute('''
                        UPDATE Inventario
                        SET Cantidad_Stock = Cantidad_Stock - ?
                        WHERE Codigo = ?
                    ''', (cantidad_movida, id_producto))
                    
                conn.commit()
                st.success('Movimiento agregado correctamente.')
            else:
                st.error(f'El producto seleccionado "{id_producto_seleccionado}" no existe.')
    except sqlite3.Error as e:
        st.error(f'Error al agregar el movimiento: {e}')

# Mostrar los datos de la tabla Movimientos_inventario con la descripción del producto
st.write('### Movimientos de Inventario:')
cursor.execute('''
    SELECT MI.ID_Movimiento, P.Nombre, MI.Tipo_Movimiento, MI.Cantidad_Movida, MI.Fecha_Hora_Movimiento, MI.Usuario, MI.Razon_Movimiento
    FROM Movimientos_inventario MI
    JOIN Productos P ON MI.Codigo = P.Codigo
''')
movimientos = cursor.fetchall()

if movimientos:
    st.table(movimientos)
else:
    st.info('No hay movimientos registrados.')

# Cerrar la conexión a la base de datos
conn.close()
