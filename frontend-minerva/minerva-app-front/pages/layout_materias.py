import streamlit as st
from utils import setup_logged_css
from menu import menu_with_redirect


setup_logged_css() # define a cor do fundo e tira a sidebar

nome_da_materia = "Teste"
largura_logo_home = 150

st.set_page_config(page_title=nome_da_materia, page_icon="./images/Minerva_logo.jpeg")   # define qual nome a aba vai ter no navegador

menu_with_redirect()

col1, mid, col2 = st.columns([1, 10, 1])    # coloca a logo e o nome no topo da pagina
with mid:
    col_logo, col_nome = st.columns([1, 3])
    with col_logo:
        st.image("./images/Minerva_logo.jpeg", width= largura_logo_home)            
    with col_nome:
        st.title("Minerva")

st.title(nome_da_materia)
st.write("Conteudo da materia:")
st.write("Tarefas:")
