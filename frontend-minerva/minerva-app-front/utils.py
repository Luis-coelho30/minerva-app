import streamlit as st
import re

def setup_css(): # define a cor do fundo, somente usado antes do usuario ter logado
    st.markdown(
        """
        <style>
            .stApp {
                background-color: #112236;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

def setup_logged_css(): # define a cor do fundo e define o topo da pagina mais pra cima, somente usado apos o login
    st.markdown(
        """
        <style>
            /* Reduz o padding no topo do container principal */
            .block-container {
                padding-top: 2rem; /* Ajuste este valor para mais ou menos espaço */
            }
            .stApp {
                background-color: #112236
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def verificar_email(email): # ve se o email fornecido esta em formato de email
    padrao = r"(^[\w][\w_.+-]+){1,}@[\w_.-]+\.[\w]{2,}$"
    return re.search(padrao, email) is not None

def verificar_senha_forte(senha):   # ve se a senha e forte (possui letra maiuscula, minuscula, numero)
    if len(senha) < 8:
        return "A senha deve conter pelo menos 8 caracteres."
    if not re.search(r"\d", senha):
        return "A senha deve conter pelo menos um número."
    if not re.search(r"[A-Z]", senha):
        return "A senha deve conter pelo menos uma letra maiúscula."
    if not re.search(r"[a-z]", senha):
        return "A senha deve conter pelo menos uma letra minúscula."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", senha):
        return "A senha deve conter pelo menos um caractere especial."
    return True
