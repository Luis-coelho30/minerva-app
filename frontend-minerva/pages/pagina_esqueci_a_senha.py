import streamlit as st
from utils import verificar_email, setup_css

setup_css() # define a cor do fundo e tira a sidebar


st.set_page_config(page_title="Recuperação", page_icon="./images/Minerva_logo.jpeg") # define qual nome a aba vai ter no navegador


largura_logo_abertura = 150

col1, mid, col2 = st.columns([1, 10, 1])    # coloca a logo e o nome no topo da pagina
with mid:
    st.image("./images/Minerva_logo.jpeg", width= largura_logo_abertura)
    st.title("Minerva")
    st.write("Recuperar sua conta")
    email_de_recuperacao = st.text_input("Email para recuperação")

    if st.button("Avançar"):
        if not verificar_email(email_de_recuperacao):
            st.error("Email inválido")
        else:
            st.switch_page("./pages/pagina_de_login.py")

    if st.button("Voltar"):
        st.switch_page("./pages/pagina_de_login.py")