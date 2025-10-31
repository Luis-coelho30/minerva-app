import streamlit as st
import datetime
from utils import setup_logged, initialize_session_state
from menu import menu_with_redirect
from components import tarefa_component
from init_session import ensure_session_state
from datetime import datetime as dt

initialize_session_state()
ensure_session_state()

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("styles/pagina_de_tarefas.css")
task_api = st.session_state.task_api
disc_api = st.session_state.disc_api

hoje = datetime.date.today()
opcoes_status = ["Pendente", "Em Progresso", "Concluída"]
opcoes_prioridade = ["Baixa", "Média", "Alta"]

st.set_page_config(page_title="Tarefas",
                   page_icon="./images/Minerva_logo.jpeg",
                   layout="wide"
                   )

setup_logged()
menu_with_redirect()

if "tarefas" not in st.session_state:
    st.session_state.tarefas = task_api.list_user_tasks()

with st.expander(icon=":material/add:", label="Adicionar Nova Tarefa", expanded=False):
    with st.form("nova_tarefa_form", clear_on_submit=True):
        disciplinas_lista = disc_api.list_user_discipline()
        disciplinas_map = {d["nome"]: d["id"] for d in disciplinas_lista}
        opcoes_disciplina_nomes = [""] + list(disciplinas_map.keys())

        titulo = st.text_input("Título da Tarefa")
        descricao = st.text_area("Descrição (Opcional)")
        status = st.selectbox("Status", opcoes_status)
        disciplina_nome_selecionada = st.selectbox("Disciplina", opcoes_disciplina_nomes)
        prioridade = st.selectbox("Prioridade", opcoes_prioridade)
        data_inicio = st.date_input("Data de Início (Opcional)", value=None, min_value = hoje)
        min_data_final = data_inicio if data_inicio is not None else hoje
        data_final = st.date_input("Data Final (Opcional)", value=None, min_value = min_data_final)

        submitted = st.form_submit_button("Adicionar Tarefa")

        if submitted and titulo:
            disciplinaId = disciplinas_map.get(disciplina_nome_selecionada)
            data_inicio_val = data_inicio.strftime("%d/%m/%Y") if data_inicio else None
            data_final_val = data_final.strftime("%d/%m/%Y") if data_final else None

            payload_criacao = {
                "titulo": titulo,
                "descricao": descricao if descricao else "",
                "status": status,
                "disciplinaId": disciplinaId,
                "dataInicio": data_inicio_val,
                "dataFinal": data_final_val,
                "concluido_em": None,
                "prioridade": prioridade,
                "arquivada": False
            }
            print(payload_criacao)

            try:
                response = task_api.create_task(payload_criacao)
                nova_tarefa = response
                st.session_state.tarefas.append(nova_tarefa)
                st.success(f"Tarefa '{titulo}' adicionada com sucesso!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao criar tarefa: {e}")

st.markdown("---")

def handle_iniciar_edicao(tarefa_obj):
    st.session_state.editando_tarefa = tarefa_obj


def handle_concluir_tarefa(tarefa_id):
    try:
        tarefa_original = None
        for t in st.session_state.tarefas:
            if t["id"] == tarefa_id:
                tarefa_original = t
                break

        if not tarefa_original:
            st.error(f"Não foi possível encontrar a tarefa (ID: {tarefa_id}) para concluir.")
            return

        payload_completo = tarefa_original.copy()
        if "id" in payload_completo:
            del payload_completo["id"]

        payload_completo["status"] = "Concluída"
        payload_completo["concluido_em"] = hoje.strftime("%d/%m/%Y")

        tarefa_atualizada_api = task_api.update_task(tarefa_id, payload_completo)

        for i, t in enumerate(st.session_state.tarefas):
            if t["id"] == tarefa_id:
                st.session_state.tarefas[i] = tarefa_atualizada_api
                break

        st.toast("Tarefa concluída!", icon="🎉")

    except Exception as e:
        st.error(f"Erro ao concluir tarefa: {e}")


def handle_excluir_tarefa(tarefa_id):
    try:
        task_api.delete_task(tarefa_id)

        # 2. Atualizar estado local
        st.session_state.tarefas = [t for t in st.session_state.tarefas if t["id"] != tarefa_id]

        st.toast("Tarefa excluída.", icon="🗑️")

    except Exception as e:
        st.error(f"Erro ao excluir tarefa: {e}")

# Exibir tarefas
if not st.session_state.tarefas:
    st.success("Ótimo trabalho! Nenhuma tarefa pendente. ✨")
else:
    for tarefa in st.session_state.tarefas:
        # CORREÇÃO: Chamada ao componente refatorado
        tarefa_component(
            tarefa=tarefa,
            on_editar=handle_iniciar_edicao,
            on_concluir=handle_concluir_tarefa,
            on_excluir=handle_excluir_tarefa
        )


@st.dialog("Editar Tarefa")
def editar_tarefa_modal():
    tarefa = st.session_state.editando_tarefa

    disciplinas_lista = disc_api.list_user_discipline()
    disciplinas_map = {d["nome"]: d["id"] for d in disciplinas_lista}
    opcoes_disciplina_nomes = [""] + list(disciplinas_map.keys())

    disciplina_atual_nome = ""
    if tarefa.get("disciplinaId"):
        for nome, id_disciplina in disciplinas_map.items():
            if id_disciplina == tarefa["disciplinaId"]:
                disciplina_atual_nome = nome
                break

    with st.form("editar_tarefa_form"):
        novo_titulo = st.text_input("Título da Tarefa", value=tarefa["titulo"])
        nova_descricao = st.text_area("Descrição", value=tarefa["descricao"] or "")
        novo_status = st.selectbox("Status",
                                   opcoes_status,
                                   index=opcoes_status.index(tarefa["status"])
                                   )

        nova_disciplina_nome = st.selectbox("Disciplina",
                                            opcoes_disciplina_nomes,
                                            index=opcoes_disciplina_nomes.index(disciplina_atual_nome) if disciplina_atual_nome else 0)

        nova_prioridade = st.selectbox("Prioridade",
                                       opcoes_prioridade,
                                       index=opcoes_prioridade.index(tarefa["prioridade"])
                                       )

        # Converter strings de data para objetos date se existirem
        data_inicio_value = dt.strptime(tarefa["dataInicio"], "%d/%m/%Y").date() if tarefa.get("dataInicio") else None
        data_final_value = dt.strptime(tarefa["dataFinal"], "%d/%m/%Y").date() if tarefa.get("dataFinal") else None

        nova_data_inicio = st.date_input("Data de Início (Opcional)", value=data_inicio_value, min_value=hoje)
        min_nova_data_final = nova_data_inicio if nova_data_inicio is not None else hoje
        nova_data_final = st.date_input("Data Final (Opcional)", value=data_final_value, min_value=min_nova_data_final)

        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Salvar"):
                tarefa_id = tarefa["id"]

                payload_completo = tarefa.copy()

                if "id" in payload_completo:
                    del payload_completo["id"]

                novo_disciplina_id = disciplinas_map.get(nova_disciplina_nome)
                data_inicio_str = nova_data_inicio.strftime("%d/%m/%Y") if nova_data_inicio else None
                data_final_str = nova_data_final.strftime("%d/%m/%Y") if nova_data_final else None

                novo_concluido_em = tarefa.get("concluido_em")
                status_original = tarefa.get("status")

                if novo_status == "Concluída" and status_original != "Concluída":
                    novo_concluido_em = hoje.strftime("%d/%m/%Y")

                elif novo_status != "Concluída" and status_original == "Concluída":
                    novo_concluido_em = None

                payload_completo.update({
                    "titulo": novo_titulo,
                    "descricao": nova_descricao,
                    "status": novo_status,
                    "disciplinaId": novo_disciplina_id,
                    "prioridade": nova_prioridade,
                    "dataInicio": data_inicio_str,
                    "dataFinal": data_final_str,
                    "concluido_em": novo_concluido_em
                })

                try:
                    tarefa_atualizada_api = task_api.update_task(tarefa_id, payload_completo)

                    for i, t in enumerate(st.session_state.tarefas):
                        if t["id"] == tarefa_id:
                            st.session_state.tarefas[i] = tarefa_atualizada_api
                            break

                    del st.session_state.editando_tarefa
                    st.success("Tarefa atualizada!")
                    st.rerun()

                except Exception as e:
                    st.error(f"Erro ao atualizar tarefa: {e}")

        with col2:
            if st.form_submit_button("Cancelar"):
                del st.session_state.editando_tarefa
                st.rerun()


# Verificar se deve abrir modal de edição
if "editando_tarefa" in st.session_state:
    editar_tarefa_modal()