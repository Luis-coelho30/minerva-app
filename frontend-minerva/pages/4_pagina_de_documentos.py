import streamlit as st
from utils import setup_logged
from menu import menu_with_redirect
from pathlib import Path
from components.documento_component import documento_component, editar_documento_modal

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(page_title="Documentos", page_icon="./images/Minerva_logo.jpeg", layout="wide")

setup_logged()
menu_with_redirect()

load_css("styles/pagina_de_documentos.css")

# Inicializar lista de documentos
if "documentos" not in st.session_state:
    st.session_state.documentos = []

with st.expander(icon=":material/add:", label="Adicionar arquivo"):
    with st.form("nova_disciplina_form", clear_on_submit=True):
        nome = st.text_input("Nome do arquivo")
        descricao = st.text_area("Descrição (Opcional)")
        disciplina = st.selectbox("Disciplina", options=[1,2], index=None)
        arquivo = st.file_uploader("", label_visibility="collapsed")
        if arquivo is not None:
            tipo = Path(arquivo.name).suffix
        enviado = st.form_submit_button("Adicionar arquivo")
        
        if enviado and nome and arquivo:
            novo_documento = {
                "nome": nome,
                "descricao": descricao,
                "disciplina": str(disciplina),
                "tipo": tipo,
                "data_upload": "Hoje",
                "arquivo_bytes": arquivo.getvalue()
            }
            st.session_state.documentos.append(novo_documento)
            st.success(f"Documento '{nome}' adicionado!")
            st.rerun()

st.markdown("---")

# Exibir documentos
if not st.session_state.documentos:
    st.success("Nenhum documento adicionado ainda.")
else:
    for doc in st.session_state.documentos:
        documento_component(**doc)

# Verificar se deve abrir modal de edição
if "editando_documento" in st.session_state:
    editar_documento_modal()
