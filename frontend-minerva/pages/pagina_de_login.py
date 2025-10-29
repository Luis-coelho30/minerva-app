import streamlit as st
from utils import setup_css

st.set_page_config(page_title="Login", page_icon="./images/Minerva_logo.jpeg") # define qual nome a aba vai ter no navegador

setup_css() # define a cor do fundo e tira a sidebar

# CSS para estilizar os botões
st.markdown("""
    <style>
    .stButton > button {
        background-color: white !important;
        color: #112236 !important;
        border: 2px solid white !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }
    .stButton > button:hover {
        background-color: #f0f0f0 !important;
        color: #112236 !important;
        border: 2px solid #f0f0f0 !important;
        font-weight: bold !important;
    }
    /* Estilizar campos de input */
    .stTextInput > div > div > input {
        background-color: white !important;
        color: #112236 !important;
        border: 2px solid white !important;
        border-radius: 8px !important;
    }
    .stTextInput > div > div > input:focus {
        background-color: white !important;
        color: #112236 !important;
        border: 2px solid #cccccc !important;
    }
    /* Estilizar labels dos inputs */
    .stTextInput > label {
        color: white !important;
        font-weight: bold !important;
    }
    /* Estilizar TODOS os containers dos inputs */
    .stTextInput > div > div,
    .stTextInput > div > div > div,
    .stTextInput div[data-baseweb="input"] {
        background-color: white !important;
    }
    /* Estilizar botão do olho */
    .stTextInput button,
    .stTextInput button > div,
    .stTextInput [data-testid="baseButton-secondary"] {
        background-color: white !important;
        color: #112236 !important;
        border: none !important;
    }
    .stTextInput button:hover {
        background-color: #f0f0f0 !important;
        color: #112236 !important;
    }
    </style>
""", unsafe_allow_html=True)

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
            st.session_state.role = 'logado'
            st.switch_page("./pages/1_pagina_home.py")
        else:
            st.error("Preencha todos os campos")

    if st.button("Voltar"):
        st.switch_page("./pages/pagina_de_abertura.py")