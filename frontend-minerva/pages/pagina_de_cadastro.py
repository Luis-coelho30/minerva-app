import streamlit as st
import re
from utils import verificar_email, verificar_senha_forte, setup_css

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

st.set_page_config(page_title="Cadastro", page_icon="./images/Minerva_logo.jpeg")   # define qual nome a aba vai ter no navegador 

col1, mid, col2 = st.columns([1, 10, 1])    # coloca a logo e o nome no topo da pagina
with mid:
    # Centralizar apenas a imagem
    _, img_col, _ = st.columns([1, 1, 1])
    with img_col:
        st.image("./images/Minerva_logo.jpeg", width=150)
    usuario = st.text_input("Usuário")
    email = st.text_input("Email")  
    senha = st.text_input("Senha", type="password")
    confirmar_senha = st.text_input("Confirmar senha", type="password")
    
    if st.button("Cadastrar"):
        resultado_senha = verificar_senha_forte(senha)  # verifica se a senha no campo e forte

        if not usuario: # verifica se o campo do usuario esta vazio
            st.error("Usuário inválido!")
        elif not verificar_email(email):    # verifica se tem um email e se ele esta num formato valido
            st.error("Email inválido!")
        elif not senha or not confirmar_senha:  # verifica se os campos das senhas estao preenchidos
            st.error("Preencha e confirme sua senha!")
        elif senha != confirmar_senha:  # verifica se as senhas sao iguais para prosseguir
            st.error("As senhas não coincidem")
        elif resultado_senha is not True:   # verifica se o resultado da funcao que ve se a senha e forte e verdadeiro
            st.error(resultado_senha)
        else:
            # Todas as validações passaram
            st.success("Cadastro realizado com sucesso! Redirecionando...")
            st.switch_page("./pages/pagina_de_abertura.py")
    if st.button("Voltar"):
        st.switch_page("./pages/pagina_de_abertura.py")