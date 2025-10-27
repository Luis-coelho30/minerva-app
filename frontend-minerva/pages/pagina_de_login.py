import streamlit as st
from utils import setup_css

st.set_page_config(page_title="Login", page_icon="./images/Minerva_logo.jpeg") # define qual nome a aba vai ter no navegador

setup_css() # define a cor do fundo e tira a sidebar

largura_logo_abertura = 150

col1, mid, col2 = st.columns([1, 10, 1])    # coloca a logo e o nome no topo da pagina
with mid:
    st.image("./images/Minerva_logo.jpeg", width= largura_logo_abertura)
    st.title("Minerva")
    st.write("Entrar na sua conta")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")


    if st.button("Esqueci a senha"):
        st.switch_page("./pages/pagina_esqueci_a_senha.py")

    if st.button("Entrar", key="entrar_login"):
        if usuario != "" and senha != "":
            st.session_state.role = 'logado'
            st.switch_page("./pages/1_pagina_home.py")
        else:
            st.error("Usuario ou senha invalidos")

    if st.button("Voltar"):
        st.switch_page("./pages/pagina_de_abertura.py")