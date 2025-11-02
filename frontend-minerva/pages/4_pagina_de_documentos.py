import streamlit as st
import datetime
from utils import setup_logged, initialize_session_state
from menu import menu_with_redirect
from pathlib import Path
from components.documento_component import documento_component
from init_session import ensure_session_state

initialize_session_state()
ensure_session_state()

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(page_title="Documentos", page_icon="./images/Minerva_logo.jpeg", layout="wide")

setup_logged()
menu_with_redirect()

load_css("styles/pagina_de_documentos.css")

disc_api = st.session_state.disc_api
file_api = st.session_state.file_api

# Inicializar lista de documentos
if "documentos" not in st.session_state:
    st.session_state.documentos = []
    #st.session_state.documentos = file_api.list_files()

with st.expander(icon=":material/add:", label="Adicionar arquivo"):
    with st.form("novo_arquivo_form", clear_on_submit=True):
        disciplinas_lista = disc_api.list_user_discipline()
        disciplinas_map = {d["nome"]: d["id"] for d in disciplinas_lista}
        opcoes_disciplina_nomes = [""] + list(disciplinas_map.keys())

        nome = st.text_input("Nome do arquivo")
        disciplina = st.selectbox("Disciplina", options=opcoes_disciplina_nomes, index=None)
        arquivo = st.file_uploader("Arquivo", label_visibility="collapsed")
        if arquivo is not None:
            tipo = Path(arquivo.name).suffix
        enviado = st.form_submit_button("Adicionar arquivo")

        if enviado and nome and arquivo:
            disciplinaId = disciplinas_map.get(disciplina)

            novo_documento = {
                "id": f"temp_{datetime.datetime.now().timestamp()}",
                "nomeOriginal": nome,
                "disciplinaId": disciplinaId,
                "tipo": tipo,
                "url": "#"
            }
            st.session_state.documentos.append(novo_documento)
            #file_api.create_file(novo_documento)
            st.success(f"Documento '{nome}' adicionado!")
            st.rerun()

st.markdown("---")

def handle_iniciar_edicao_doc(documento_obj):
    st.session_state.editando_documento = documento_obj


def handle_excluir_doc(doc_id):


    try:
        # file_api.delete_file(doc_id)

        st.session_state.documentos = [
            d for d in st.session_state.documentos if d.get("id") != doc_id
        ]
        st.toast("🗑️ Documento excluído!")

    except Exception as e:
        st.error(f"Erro ao excluir documento: {e}")

# Prepara as disciplinas para mostrar na pagina
disciplinas_lista = disc_api.list_user_discipline()
disciplinas_map_nome_id = {d["nome"]: d["id"] for d in disciplinas_lista}
opcoes_disciplina_nomes = [""] + list(disciplinas_map_nome_id.keys())
disciplinas_map_id_nome = {d["id"]: d["nome"] for d in disciplinas_lista}

st.markdown("---")

if "documentos" not in st.session_state or not st.session_state.documentos:
    st.info("Nenhum documento adicionado.")
else:
    for doc in st.session_state.documentos:
        disciplina_id_do_doc = doc.get("disciplinaId")
        nome_da_disciplina = disciplinas_map_id_nome.get(disciplina_id_do_doc, "")

        documento_component(
            documento=doc,
            on_editar=handle_iniciar_edicao_doc,
            on_excluir=handle_excluir_doc,
            disciplina_nome=nome_da_disciplina
        )

@st.dialog("Editar Documento")
def editar_documento_modal():
    doc = st.session_state.editando_documento

    disciplina_atual_nome = disciplinas_map_id_nome.get(doc.get("disciplinaId"), "")

    with st.form("editar_documento_form"):
        novo_nome = st.text_input("Nome do arquivo", value=doc.get("nomeOriginal", ""))

        nova_disciplina_nome = st.selectbox("Disciplina",
                                            options=opcoes_disciplina_nomes,
                                            index=opcoes_disciplina_nomes.index(
                                                disciplina_atual_nome) if disciplina_atual_nome else 0)

        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Salvar"):

                novo_disciplina_id = disciplinas_map_nome_id.get(nova_disciplina_nome)

                # file_api.update_file(doc["id"], payload)

                for i, d in enumerate(st.session_state.documentos):
                    if d.get("id") == doc["id"]:
                        st.session_state.documentos[i].update({
                            "nomeOriginal": novo_nome,
                            "disciplinaId": novo_disciplina_id
                        })
                        break

                del st.session_state.editando_documento
                st.success("Documento atualizado!")
                st.rerun()

        with col2:
            if st.form_submit_button("Cancelar"):
                del st.session_state.editando_documento
                st.rerun()

if "editando_documento" in st.session_state:
    editar_documento_modal()