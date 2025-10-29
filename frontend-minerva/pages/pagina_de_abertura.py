import streamlit as st
from utils import setup_css

st.set_page_config(page_title="Minerva", page_icon="./images/Minerva_logo.jpeg")

setup_css() # define a cor do fundo e tira a sidebar

# CSS específico para esta página
st.markdown("""
    <style>
    .stImage {
        margin-left: -40px !important;
    }
    /* Estilizar botões */
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
    }
    </style>
""", unsafe_allow_html=True)

# Adiciona espaço entre as colunas
col_esquerda, col_meio, col_direita = st.columns([2.5, 0.5, 2.5])

# Coluna da esquerda - Logo e descrição
with col_esquerda:
    st.markdown("<br>", unsafe_allow_html=True)  # Mais espaço no topo
    st.image("images/Minerva_logo.jpeg", width=330)
    st.markdown("<h2 style='text-align: center; color: white; margin-top: -30px;'>Minerva</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: white; margin-top: -15px; font-size: 18px; '>Organização que impera!</h4>", unsafe_allow_html=True)

# Coluna do meio - Espaço vazio
with col_meio:
    st.write("")  # Coluna vazia para criar espaço

# Coluna da direita - Botões
with col_direita:
    st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)  # Espaço no topo
    
    st.markdown("<h3 style='text-align: center; color: white; margin-bottom: 30px; margin-left: +22px;'>Acesse sua conta</h3>", unsafe_allow_html=True)
    
    if st.button("Entrar", use_container_width=True, key="login_btn"):
        st.switch_page("./pages/pagina_de_login.py")
    
    if st.button("Cadastrar", use_container_width=True, key="register_btn"):
        st.switch_page("./pages/pagina_de_cadastro.py")
