import streamlit as st
import re
import pandas as pd

# Bloco de CSS pra tirar a barra lateral 
st.markdown(
    """
    <style>
        .stApp {
            background-color: #112236
        }
    
        
    </style>
    """,
    unsafe_allow_html=True,
)

largura_logo_abertura = 150
largura_logo_home = 100

def pagina_de_abertura():
    col1, mid, col2 = st.columns([1, 10, 1])
    with mid:
        st.image("images/Minerva_logo.jpeg", width= largura_logo_abertura)
        st.title("Minerva")
        st.write("Bem-vindo ao app de organização acadêmica!")
        
        if st.button("Entrar"):
            st.session_state["pagina_atual"] = 'login'
            st.rerun()

        if st.button("Cadastrar"):
            st.session_state["pagina_atual"] = "cadastro"
            st.rerun()


def pagina_de_login():
    col1, mid, col2 = st.columns([1, 10, 1])
    with mid:
        st.image("images/Minerva_logo.jpeg", width= largura_logo_abertura)
        st.title("Minerva")
        st.write("Entrar na sua conta")
    
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")

        if st.button("Esqueci a senha"):
            st.session_state["pagina_atual"] = "esqueci_a_senha"
            st.rerun()

        if st.button("Entrar", key="entrar_login"):
            if usuario != "" and senha != "":
                st.session_state["pagina_atual"] = "home"
                st.rerun()
            else:
                st.error("Usuario ou senha invalidos")

        if st.button("Voltar"):
            st.session_state["pagina_atual"] = "abertura"
            st.rerun()

def pagina_de_cadastro():
    col1, mid, col2 = st.columns([1, 10, 1])
    with mid:
        st.image("images/Minerva_logo.jpeg", width= largura_logo_abertura)
        st.title("Minerva")

        st.write("Cadastrar uma conta")
        usuario = st.text_input("Usuário")
        email = st.text_input("Email")  
        senha = st.text_input("Senha", type="password")
        confirmar_senha = st.text_input("Confirmar senha", type="password")
        if st.button("Cadastrar"):
            resultado_senha = verificar_senha_forte(senha)

            if not usuario:
                st.error("Preencha o campo do Usuário")
            elif not verificar_email(email):
                st.error("Email inválido")
            elif not senha or not confirmar_senha:
                st.error("Preencha e confirme sua senha")
            elif senha != confirmar_senha:
                st.error("As senhas não coincidem")
            elif resultado_senha is not True:
                st.error(resultado_senha)
            else:
                # Todas as validações passaram
                st.success("Cadastro realizado com sucesso! Redirecionando...")
                st.session_state["pagina_atual"] = "abertura"
                st.rerun()

def pagina_esqueci_a_senha():
    col1, mid, col2 = st.columns([1, 10, 1])
    with mid:
        st.image("images/Minerva_logo.jpeg", width= largura_logo_abertura)
        st.title("Minerva")
        st.write("Recuperar sua conta")
        email_de_recuperacao = st.text_input("Email para recuperação")

        if st.button("Avançar"):
            if not verificar_email(email_de_recuperacao):
                st.error("Email inválido")
            else:
                st.session_state["pagina_atual"] = "login"
                st.rerun()
    
        if st.button("Voltar"):
            st.session_state["pagina_atual"] = "login"
            st.rerun()

def pagina_home():
    st.markdown(
    """
    <style>
        /* Reduz o padding no topo do container principal */
        .block-container {
            padding-top: 1rem; /* Ajuste este valor para mais ou menos espaço */
        }
        .stApp {
            background-color: #112236
        }
    </style>
    """,
    unsafe_allow_html=True,
)
    col1, mid, col2 = st.columns([1, 10, 1])
    with mid:
        col_logo, col_nome = st.columns([1, 3])
        with col_logo:
            st.image("images/Minerva_logo.jpeg", width= largura_logo_home)            
        with col_nome:
            st.title("Minerva")


        
def verificar_email(email):
    valido = False
    padrao = r"(^[\w][\w_.+-]+){1,}@[\w_.-]+\.[\w]{2,}$"
    if re.search(padrao, email):
        valido = True
    return valido

def verificar_senha_forte(senha):
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


if "pagina_atual" not in st.session_state:
    st.session_state["pagina_atual"] = "abertura"

if st.session_state["pagina_atual"] == "abertura":
    pagina_de_abertura()
elif st.session_state["pagina_atual"] == "login":
    pagina_de_login()
elif st.session_state["pagina_atual"] == "cadastro":
    pagina_de_cadastro()
elif st.session_state["pagina_atual"] == "esqueci_a_senha":
    pagina_esqueci_a_senha()
elif st.session_state["pagina_atual"] == "home":
    pagina_home()