import streamlit as st
import sqlite3

# Conectar a la base de datos SQLite
conn = sqlite3.connect('inventario.db')
c = conn.cursor()

# Crear la tabla Productos si no existe
c.execute('''
    CREATE TABLE IF NOT EXISTS Productos (
        ID_Producto INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre TEXT,
        Descripcion TEXT,
        Precio_Compra REAL,
        Precio_Venta REAL,
        Categoria_id INTEGER,
        Proveedor TEXT,
        Unidad_Medida TEXT
    )
''')


# Crear la tabla Categorias si no existe
c.execute('''
    CREATE TABLE IF NOT EXISTS Categorias (
        ID_Categoria INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre_Categoria TEXT
    )
''')

# Función para obtener las categorías
def obtener_categorias():
    c.execute('SELECT ID_Categoria, Nombre_Categoria FROM Categorias')
    categorias = c.fetchall()
    return categorias

# Función para insertar un nuevo producto
def insertar_producto(nombre, descripcion, precio_compra, precio_venta, categoria_id, proveedor, unidad_medida):
    c.execute('INSERT INTO Productos (Nombre, Descripcion, Precio_Compra, Precio_Venta, Categoria, Proveedor, Unidad_Medida) VALUES (?, ?, ?, ?, ?, ?, ?)',
              (nombre, descripcion, precio_compra, precio_venta, categoria_id, proveedor, unidad_medida))
    conn.commit()

# Crear la aplicación Streamlit
def main():
    st.title('Ingreso de Productos')

    # Obtener las categorías disponibles
    categorias = obtener_categorias()
    nombres_categorias = [categoria[1] for categoria in categorias]

    # Formulario para ingresar un nuevo producto
    st.header('Nuevo Producto')
    nombre = st.text_input('Nombre del Producto')
    descripcion = st.text_area('Descripción')
    precio_compra = st.number_input('Precio de Compra', step=0.01)
    precio_venta = st.number_input('Precio de Venta', step=0.01)
    categoria = st.selectbox('Categoría', nombres_categorias)
    proveedor = st.text_input('Proveedor')
    unidad_medida = st.text_input('Unidad de Medida')

    if st.button('Guardar Producto'):
        # Obtener el ID de la categoría seleccionada
        categoria_id = categorias[nombres_categorias.index(categoria)][0]

        # Insertar el producto en la base de datos
        insertar_producto(nombre, descripcion, precio_compra, precio_venta, categoria_id, proveedor, unidad_medida)

        # Mostrar el producto ingresado
        st.success(f'Producto Guardado: {nombre}, Categoría: {categoria}')

        # Mostrar el último producto ingresado
        st.header('Último Producto Ingresado')
        st.write(f'Nombre: {nombre}, Categoría: {categoria}')

if __name__ == '__main__':
    main()
