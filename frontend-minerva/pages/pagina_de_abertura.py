import streamlit as st
from utils import setup_css
from pathlib import Path

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

setup_css()
BASE_DIR = Path(__file__).parent.parent
style_path = BASE_DIR / "styles" / "pagina_de_abertura.css"
image_path = BASE_DIR / "images" / "Minerva_logo.jpeg"
pagina_de_cadastro_path = BASE_DIR / "pages" / "pagina_de_cadastro.py"
pagina_de_login_path = BASE_DIR / "pages" / "pagina_de_login.py"
load_css(style_path)

st.set_page_config(page_title="Minerva", page_icon=image_path)

col_esquerda, col_meio, col_direita = st.columns([2.5, 0.5, 2.5])

with col_esquerda:
    st.markdown("<br>", unsafe_allow_html=True)  
    st.image(image_path, width=330)
    st.markdown("<h2 style='text-align: center; color: white; margin-top: -30px;'>Minerva</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: white; margin-top: -15px; font-size: 18px; '>Organização que impera!</h4>", unsafe_allow_html=True)

with col_meio:
    st.write("") 

with col_direita:
    st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: white; margin-bottom: 30px; margin-left: +22px;'>Acesse sua conta</h3>", unsafe_allow_html=True)
    
    if st.button("Entrar", use_container_width=True, key="login_btn"):
        st.switch_page(pagina_de_login_path)
    
    if st.button("Cadastrar", use_container_width=True, key="register_btn"):
        st.switch_page(pagina_de_cadastro_path)