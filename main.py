import streamlit as st
from st_pages import Page, show_pages, add_page_title

st.title("SISTEMA DE CONTROL DE INVENTARIO")

show_pages([
    Page("main.py", "Inicio"),
    Page("cargaproductos.py", "Cargar Productos"),
    Page("cargarproveedores.py", "Cargar Proveedores"),
    Page("categorias.py", "Cargar Categorías"),
    Page("productos.py", "Productos"),
    Page("cargamovimientos.py", "Movimientos"),
    ])
