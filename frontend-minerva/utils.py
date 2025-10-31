import streamlit as st
import re
from api_client.client import ApiClient
from api_client.endpoints.UserEndpoint import UserEndpoint
from api_client.endpoints.TaskEndpoint import TaskEndpoint
from api_client.endpoints.DisciplineEndpoint import DisciplinaEndpoint
from api_client.endpoints.GradeEndpoint import GradeEndpoint
from api_client.endpoints.FileEndpoint import FileEndpoint

def setup_css():
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

def setup_logged(): # define a cor do fundo e define o topo da pagina mais pra cima, somente usado apos o login
    largura_logo_home = 150
    st.markdown(
        """
        <style>
            /* Reduz o padding no topo do container principal */
            .block-container {
                padding-top: 5rem; /* Ajuste este valor para mais ou menos espaço */
            }
            .stApp {
                background-color: #112236
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    _, mid, _ = st.columns([2, 3, 2])
    with mid:
        # Centralizar apenas a logo
        _, logo_col, _ = st.columns([1, 1, 1])
        with logo_col:
            st.image("./images/Minerva_logo.jpeg", width=400)

@st.cache_resource
def init_api_clients():
    client = ApiClient(base_url="http://localhost:8080")
    return {
        "client": client,
        "user_api": UserEndpoint(client),
        "task_api": TaskEndpoint(client),
        "disc_api": DisciplinaEndpoint(client),
        "grade_api": GradeEndpoint(client),
        "file_api": FileEndpoint(client)
    }


def initialize_session_state():
    if "client" not in st.session_state:
        apis = init_api_clients()
        st.session_state.update(apis)

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
