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
    
        [data-testid="stSidebar"] {
            display: none;
        }
        [data-testid="collapsedControl"] {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
largura_logo=150

def pagina_de_abertura():
    col1, mid, col2 = st.columns([1, 10, 1])
    with mid:
        st.image("images/Minerva_logo.jpeg", width= largura_logo)
        st.title("Minerva",width=200)
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
        st.image("images/Minerva_logo.jpeg", width= largura_logo)
    
        st.title("Minerva",width=200)
        st.write("Entrar na sua conta")
    
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")

        if st.button("Esqueci a senha"):
            st.session_state["pagina_atual"] = "esqueci_a_senha"
            st.rerun()

        if st.button("Entrar", key="entrar_login"):
            st.success("Login realizado com sucesso! (Em construção)")

        if st.button("Voltar"):
            st.session_state["pagina_atual"] = "abertura"
            st.rerun()

def pagina_de_cadastro():
    col1, mid, col2 = st.columns([1, 10, 1])
    with mid:
        st.image("images/Minerva_logo.jpeg", width= largura_logo)
        st.title("Minerva",width=200)

        st.write("Cadastrar uma conta")
        usuario = st.text_input("Usuário")
        email = st.text_input("Email")  
        senha = st.text_input("Senha", type="password")
        confirmar_senha = st.text_input("Confirmar senha", type="password")
        if st.button("Cadastrar"):
            if usuario != "" :
                if verificar_email(email):
                    if senha and confirmar_senha != "":
                        if senha == confirmar_senha:
                            st.session_state["pagina_atual"] = "abertura"
                            st.rerun()
                        else:
                            st.error("As senhas devem ser iguais")
                    else:
                        st.error("Preencha o campo das Senhas")        
                else:
                    st.error("Email invalido")
            else:
                st.error("Preencha o campo do Usuário")

def pagina_esqueci_a_senha():
    col1, mid, col2 = st.columns([1, 10, 1])
    with mid:
        st.image("images/Minerva_logo.jpeg", width= largura_logo)
        email_de_recuperacao = st.text_input("Email para recuperação")
        if st.button("Avançar"):
            st.session_state["pagina_atual"] = "login"
            st.rerun()
            if st.button("Voltar"):
                st.session_state["pagina_atual"] = "login"
                st.rerun()
        if st.button("Voltar"):
            st.session_state["pagina_atual"] = "login"
            st.rerun()
            


        
def verificar_email(email):
    valido = False
    padrao = r"(^[\w][\w_.+-]+){1,}@[\w_.-]+\.[\w]{2,}$"
    if re.search(padrao, email):
        valido = True
    return valido


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