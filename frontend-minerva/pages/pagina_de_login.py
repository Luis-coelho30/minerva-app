import streamlit as st
from utils import setup_css, initialize_session_state
from pathlib import Path

initialize_session_state()

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

setup_css()
BASE_DIR = Path(__file__).parent.parent
print(BASE_DIR)
style_path = BASE_DIR / "styles" / "pagina_de_login.css"
image_path = BASE_DIR / "images" / "Minerva_logo.jpeg"
pagina_de_abertura_path = BASE_DIR / "pages" / "pagina_de_abertura.py"
pagina_home_path = BASE_DIR / "pages" / "1_pagina_home.py"
pagina_esqueci_a_senha_path = BASE_DIR / "pages" / "pagina_esqueci_a_senha.py"
load_css(style_path)

user_api = st.session_state.user_api

st.set_page_config(page_title="Login", page_icon=image_path) # define qual nome a aba vai ter no navegador

col1, mid, col2 = st.columns([1, 10, 1])    # coloca a logo e o nome no topo da pagina
with mid:
    # Centralizar apenas a imagem
    _, img_col, _ = st.columns([1, 1, 1])
    with img_col:
        st.image(image_path, width=150)

    usuario = st.text_input("Usuário")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")

    if st.button("Esqueci a senha"):
        st.switch_page(pagina_esqueci_a_senha_path)

    if st.button("Entrar", key="entrar_login"):
        if usuario != "" and email != "" and senha != "":
            try:
                response = user_api.login(usuario, email, senha)
                st.session_state.role = "logado"
                st.switch_page(pagina_home_path)
            except Exception as e:
                st.error(f"Email ou senha incorretos + {e}")
        else:
            st.error("Preencha todos os campos")

    if st.button("Voltar"):
        st.switch_page(pagina_de_abertura_path)