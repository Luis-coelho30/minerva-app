import streamlit as st
from utils import setup_css

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

setup_css()
load_css("styles/pagina_de_abertura.css")

st.set_page_config(page_title="Minerva", page_icon="./images/Minerva_logo.jpeg")

col_esquerda, col_meio, col_direita = st.columns([2.5, 0.5, 2.5])

with col_esquerda:
    st.markdown("<br>", unsafe_allow_html=True)  
    st.image("images/Minerva_logo.jpeg", width=330)
    st.markdown("<h2 style='text-align: center; color: white; margin-top: -30px;'>Minerva</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: white; margin-top: -15px; font-size: 18px; '>Organização que impera!</h4>", unsafe_allow_html=True)

with col_meio:
    st.write("") 

with col_direita:
    st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: white; margin-bottom: 30px; margin-left: +22px;'>Acesse sua conta</h3>", unsafe_allow_html=True)
    
    if st.button("Entrar", use_container_width=True, key="login_btn"):
        st.switch_page("./pages/pagina_de_login.py")
    
    if st.button("Cadastrar", use_container_width=True, key="register_btn"):
        st.switch_page("./pages/pagina_de_cadastro.py")