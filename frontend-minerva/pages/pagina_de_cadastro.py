import streamlit as st
import re
from utils import verificar_email, verificar_senha_forte, setup_css

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

setup_css()
load_css("styles/pagina_de_cadastro.css")

user_api = st.session_state.user_api

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
            try:
                user_resp = {
                            "username": usuario,
                            "email": email,
                            "senha": senha
                }
                resposta = user_api.create_user(user_resp)
                st.success("Cadastro realizado com sucesso! Redirecionando...")
                st.switch_page("./pages/pagina_de_abertura.py")
            except Exception as e:
                st.error(f"Erro ao cadastrar usuário: Email: {email} já foi cadastrado!")

    if st.button("Voltar"):
        st.switch_page("./pages/pagina_de_abertura.py")