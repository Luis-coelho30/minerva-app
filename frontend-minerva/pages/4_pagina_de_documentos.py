import streamlit as st
from utils import setup_logged
from menu import menu_with_redirect
from pathlib import Path

setup_logged()

menu_with_redirect()

st.set_page_config(page_title="Documentos", page_icon="./images/Minerva_logo.jpeg", layout="wide")

with st.expander(icon=":material/add:",label="Adicionar arquivo"):
     with st.form("nova_disciplina_form", clear_on_submit=True):
        nome = st.text_input("Nome do arquivo")
        descricao = st.text_area("Descrição (Opcional)")
        disciplina = st.selectbox("Disciplina", options=[1,2], index=None)
        arquivo = st.file_uploader("Selecione um arquivo")
        if arquivo is not None:
            tipo = Path(arquivo.name).suffix
        enviado = st.form_submit_button("Adicionar arquivo")
        #if nome != "" and disciplina and arquivo is not None:
            # envia os dados pro banco de dados
st.markdown("---")


