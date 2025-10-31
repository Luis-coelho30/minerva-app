import streamlit as st

from utils import setup_logged, initialize_session_state
from menu import menu_with_redirect
from components import tarefa_component
from init_session import ensure_session_state

initialize_session_state()
ensure_session_state()

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("styles/pagina_de_tarefas.css")
task_api = st.session_state.task_api
disc_api = st.session_state.disc_api

opcoes_status = ["Pendente", "Em Progresso", "Concluída"]
opcoes_prioridade = ["Baixa", "Média", "Alta"]

st.set_page_config(page_title="Tarefas",
                   page_icon="./images/Minerva_logo.jpeg")  # define qual nome a aba vai ter no navegador

setup_logged()  # define a cor de fundo e que a pagina comeca mais pra cima pra logo ficar mais alta

menu_with_redirect()

if "tarefas" not in st.session_state:
    st.session_state.tarefas = task_api.list_user_tasks()

with st.expander(icon=":material/add:", label="Adicionar Nova Tarefa", expanded=False):
    with st.form("nova_tarefa_form", clear_on_submit=True):
        disciplinas = disc_api.list_user_discipline()
        opcoes_disciplina = [""] + [d["nome"] for d in disciplinas]

        titulo = st.text_input("Título da Tarefa")
        descricao = st.text_area("Descrição (Opcional)")
        status = st.selectbox("Status", ["Pendente", "Em Progresso", "Concluída", "Cancelada"])
        disciplina = st.selectbox("Disciplina", opcoes_disciplina)
        prioridade = st.selectbox("Prioridade", ["Baixa", "Média", "Alta"])
        data_inicio = st.date_input("Data de Início (Opcional)", value=None)
        data_final = st.date_input("Data Final (Opcional)", value=None)

        submitted = st.form_submit_button("Adicionar Tarefa")

        if submitted and titulo:
            disciplinaId = None
            data_inicio_val = data_inicio.strftime("%d/%m/%Y") if data_inicio else None
            data_final_val = data_final.strftime("%d/%m/%Y") if data_final else None

            response = task_api.create_task(
                titulo=titulo,
                descricao=descricao if descricao else "",
                status=status,
                disciplinaId=disciplinaId,
                dataInicio=data_inicio_val,
                dataFim=data_final_val,
                concluido_em="",  # inicialmente vazio
                prioridade=prioridade,
                arquivada=False
            )

            nova_tarefa = response
            st.session_state.tarefas.append(nova_tarefa)
            st.success(f"Tarefa '{titulo}' adicionada com sucesso!")
            st.rerun()

st.markdown("---")

# Exibir tarefas
if not st.session_state.tarefas:
    st.success("Ótimo trabalho! Nenhuma tarefa pendente. ✨")
else:
    for tarefa in st.session_state.tarefas:
        tarefa_component(tarefa.get("titulo"),
                         tarefa.get("descricao"),
                         tarefa.get("status"),
                         tarefa.get("disciplina"),
                         tarefa.get("prioridade"),
                         tarefa.get("arquivada"),
                         tarefa.get("data_inicio"),
                         tarefa.get("data_final"),
                         tarefa.get("concluido_em"))


@st.dialog("Editar Tarefa")
def editar_tarefa_modal():
    tarefa = st.session_state.editando_tarefa
    disciplinas = disc_api.list_user_discipline()
    opcoes_disciplina = [""] + [d["nome"] for d in disciplinas]

    with st.form("editar_tarefa_form"):
        novo_titulo = st.text_input("Título da Tarefa", value=tarefa["titulo"])

        nova_descricao = st.text_area("Descrição", value=tarefa["descricao"] or "")

        novo_status = st.selectbox("Status",
                                   opcoes_status,
                                   index=opcoes_status.index(tarefa["status"])
                                   )

        nova_disciplina = st.selectbox("Disciplina", opcoes_disciplina)

        nova_prioridade = st.selectbox("Prioridade",
                                       opcoes_prioridade,
                                       index=opcoes_prioridade.index(tarefa["prioridade"])
                                       )

        # Converter strings de data para objetos date se existirem
        data_inicio_value = None
        if tarefa["data_inicio"]:
            from datetime import datetime
            data_inicio_value = datetime.strptime(tarefa["data_inicio"], "%d/%m/%Y").date()

        data_final_value = None
        if tarefa["data_final"]:
            from datetime import datetime
            data_final_value = datetime.strptime(tarefa["data_final"], "%d/%m/%Y").date()

        nova_data_inicio = st.date_input("Data de Início (Opcional)", value=data_inicio_value)
        nova_data_final = st.date_input("Data Final (Opcional)", value=data_final_value)

        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Salvar"):
                # Atualizar tarefa na lista
                for i, t in enumerate(st.session_state.tarefas):
                    if t["titulo"] == tarefa["titulo"]:
                        st.session_state.tarefas[i].update({
                            "titulo": novo_titulo,
                            "descricao": nova_descricao,
                            "status": novo_status,
                            "disciplina": nova_disciplina,
                            "prioridade": nova_prioridade,
                            "data_inicio": str(nova_data_inicio) if nova_data_inicio else None,
                            "data_final": str(nova_data_final) if nova_data_final else None
                        })
                        break
                del st.session_state.editando_tarefa
                st.success("Tarefa atualizada!")
                st.rerun()

        with col2:
            if st.form_submit_button("Cancelar"):
                del st.session_state.editando_tarefa
                st.rerun()


# Verificar se deve abrir modal de edição
if "editando_tarefa" in st.session_state:
    editar_tarefa_modal()