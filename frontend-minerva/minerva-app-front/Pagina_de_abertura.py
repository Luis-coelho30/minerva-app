
import streamlit as st
from utils import setup_css

setup_css()

st.set_page_config(page_title="Minerva", page_icon="./images/Minerva_logo.jpeg")

col1, mid, col2 = st.columns([1, 10, 1])
largura_logo_abertura = 150
with mid:
    st.image("images/Minerva_logo.jpeg", width= largura_logo_abertura)
    st.title("Minerva")
    st.write("Bem-vindo ao app de organização acadêmica!")
    
    if st.button("Entrar"):
        st.switch_page("./pages/pagina_de_login.py")

    if st.button("Cadastrar"):
        st.switch_page("./pages/pagina_de_cadastro.py")