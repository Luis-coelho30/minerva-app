import streamlit as st
from utils import setup_logged_css

largura_logo_home = 150

setup_logged_css()  # define a cor de fundo e que a pagina comeca mais pra cima pra logo ficar mais alta

st.set_page_config(page_title="Materias", page_icon="./images/Minerva_logo.jpeg")   # define qual nome a aba vai ter no navegador

col1, mid, col2 = st.columns([1, 10, 1])    # coloca a logo e o nome no topo da pagina
with mid:
    col_logo, col_nome = st.columns([1, 3])
    with col_logo:
        st.image("./images/Minerva_logo.jpeg", width= largura_logo_home)            
    with col_nome:
        st.title("Minerva")