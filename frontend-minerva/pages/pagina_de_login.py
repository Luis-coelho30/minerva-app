import streamlit as st
from utils import setup_css, initialize_session_state

initialize_session_state()

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

setup_css()
load_css("styles/pagina_de_login.css")

user_api = st.session_state.user_api

st.set_page_config(page_title="Login", page_icon="./images/Minerva_logo.jpeg") # define qual nome a aba vai ter no navegador

col1, mid, col2 = st.columns([1, 10, 1])    # coloca a logo e o nome no topo da pagina
with mid:
    # Centralizar apenas a imagem
    _, img_col, _ = st.columns([1, 1, 1])
    with img_col:
        st.image("./images/Minerva_logo.jpeg", width=150)

    usuario = st.text_input("Usuário")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")

    if st.button("Esqueci a senha"):
        st.switch_page("./pages/pagina_esqueci_a_senha.py")

    if st.button("Entrar", key="entrar_login"):
        if usuario != "" and email != "" and senha != "":
            try:
                response = user_api.login(usuario, email, senha)
                st.session_state.role = "logado"
                st.switch_page("./pages/1_pagina_home.py")
            except Exception as e:
                st.error(f"Email ou senha incorretos + {e}")
        else:
            st.error("Preencha todos os campos")

    if st.button("Voltar"):
        st.switch_page("./pages/pagina_de_abertura.py")