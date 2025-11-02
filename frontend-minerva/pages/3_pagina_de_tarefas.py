import streamlit as st
import datetime

from utils import setup_logged, initialize_session_state
from menu import menu_with_redirect
from components.tarefa_component import tarefa_component, tarefa_arquivada_component
from init_session import ensure_session_state
from datetime import datetime as dt
from pathlib import Path

initialize_session_state()
ensure_session_state()

BASE_DIR = Path(__file__).parent.parent
image_path = BASE_DIR / "images" / "Minerva_logo.jpeg"
style_path = BASE_DIR / "styles" / "pagina_de_tarefas.css"

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css(style_path)
task_api = st.session_state.task_api
disc_api = st.session_state.disc_api

hoje = datetime.date.today()
opcoes_status = ["Pendente", "Em Progresso", "Concluída"]
opcoes_prioridade = ["Baixa", "Média", "Alta"]

if "mapa_id_disc" not in st.session_state:
    try:
        disciplinas_lista = disc_api.list_user_discipline()
        st.session_state.mapa_id_disc = {d["id"]: d["nome"] for d in disciplinas_lista}
        st.session_state.mapa_disc_id = {d["nome"]: d["id"] for d in disciplinas_lista}
    except Exception as e:
        st.error(f"Erro ao carregar mapa de disciplinas: {e}")
        st.session_state.mapa_id_disc = {}
        st.session_state.mapa_disc_id = {}

st.set_page_config(page_title="Tarefas",
                   page_icon=image_path,
                   layout="wide"
                   )

setup_logged()
menu_with_redirect()

if "tarefas" not in st.session_state:
    st.session_state.tarefas = task_api.list_user_tasks()

with st.expander(icon=":material/add:", label="Adicionar Nova Tarefa", expanded=False):
    with st.form("nova_tarefa_form", clear_on_submit=True):
        opcoes_disciplina_nomes = [""] + list(st.session_state.mapa_disc_id.keys())

        titulo = st.text_input("Título da Tarefa")
        descricao = st.text_area("Descrição (Opcional)")
        col1, col2, col3 = st.columns(3)

        with col1:
            status = st.selectbox("Status", opcoes_status)

        with col2:
            disciplina_nome_selecionada = st.selectbox("Disciplina", opcoes_disciplina_nomes)

        with col3:
            prioridade = st.selectbox("Prioridade", opcoes_prioridade)

        col_data_inicio, col_data_final = st.columns(2)
        with col_data_inicio:
            data_inicio = st.date_input("Data de Início (Opcional)", value=None, min_value=hoje)

        with col_data_final:
            data_final = st.date_input("Data Final (Opcional)", value=None, min_value=hoje)

        submitted = st.form_submit_button("Adicionar Tarefa")

        if submitted and titulo:
            if data_inicio and data_final and (data_final < data_inicio):
                st.error("A data final não pode ser anterior à data de início.")

            else:
                disciplinaId = st.session_state.mapa_disc_id.get(disciplina_nome_selecionada)
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

        st.session_state.tarefas = [t for t in st.session_state.tarefas if t["id"] != tarefa_id]

        st.toast("Tarefa excluída.", icon="🗑️")

    except Exception as e:
        st.error(f"Erro ao excluir tarefa: {e}")


def handle_arquivar_tarefa(tarefa):
    try:
        tarefa_id = tarefa.get('id')
        payload = tarefa.copy()
        if "id" in payload: del payload["id"]
        payload["arquivada"] = True

        tarefa_atualizada = task_api.update_task(tarefa_id, payload)

        for i, t in enumerate(st.session_state.tarefas):
            if t["id"] == tarefa_id:
                st.session_state.tarefas[i] = tarefa_atualizada
                break

        st.toast("Tarefa arquivada.")

    except Exception as e:
        st.error(f"Erro ao arquivar: {e}")


def handle_desarquivar_tarefa(tarefa):
    try:
        tarefa_id = tarefa.get('id')
        payload = tarefa.copy()
        if "id" in payload: del payload["id"]
        payload["arquivada"] = False

        tarefa_atualizada = task_api.update_task(tarefa_id, payload)

        for i, t in enumerate(st.session_state.tarefas):
            if t["id"] == tarefa_id:
                st.session_state.tarefas[i] = tarefa_atualizada
                break

        st.toast("Tarefa desarquivada.")

    except Exception as e:
        st.error(f"Erro ao desarquivar: {e}")


def get_sort_key(tarefa):
    # Se a tarefa estiver concluída deverá ser colocada ao final
    is_concluida = 1 if tarefa.get("status") == "Concluída" else 0
    # Coleta a data final
    data_str = tarefa.get("dataFinal")
    sort_date = datetime.date.max

    if data_str:
        try:
            sort_date = datetime.datetime.strptime(data_str, "%d/%m/%Y").date()
        except (ValueError, TypeError):
            pass

    # Retorna a Tupla para ordenação com tarefas não concluídas e próximas em primeiro lugar
    return is_concluida, sort_date

# Exibir tarefas
if not st.session_state.tarefas:
    st.success("Ótimo trabalho! Nenhuma tarefa pendente. ✨")
else:
    # Separa as tarefas arquivadas das excluídas
    tarefas_ativas = [t for t in st.session_state.tarefas if not t.get('arquivada', False)]
    tarefas_arquivadas = [t for t in st.session_state.tarefas if t.get('arquivada', False)]

    # Ordena as tarefas
    tarefas_ativas_ordenadas = sorted(tarefas_ativas, key=get_sort_key)
    tarefas_arquivadas_ordenadas = sorted(tarefas_arquivadas, key=get_sort_key)

    mapa_id_para_nome = st.session_state.mapa_id_disc

    if not tarefas_ativas_ordenadas:
        st.success("Ótimo trabalho! Nenhuma tarefa pendente. ✨")
    else:
        for tarefa in tarefas_ativas_ordenadas:
            disciplina_id = tarefa.get("disciplinaId")
            nome_da_disciplina = mapa_id_para_nome.get(disciplina_id, "")
            tarefa["disciplina"] = nome_da_disciplina

            tarefa_component(
                tarefa=tarefa,
                on_editar=handle_iniciar_edicao,
                on_concluir=handle_concluir_tarefa,
                on_excluir=handle_excluir_tarefa,
                on_arquivar=handle_arquivar_tarefa
            )

    if tarefas_arquivadas_ordenadas:
        with st.expander("Tarefas Arquivadas"):
            for tarefa in tarefas_arquivadas_ordenadas:
                disciplina_id = tarefa.get("disciplinaId")
                nome_da_disciplina = mapa_id_para_nome.get(disciplina_id, "")
                tarefa["disciplina"] = nome_da_disciplina

                tarefa_arquivada_component(
                    tarefa=tarefa,
                    on_desarquivar=handle_desarquivar_tarefa,
                    on_excluir=handle_excluir_tarefa
                )


@st.dialog("Editar Tarefa")
def editar_tarefa_modal():
    tarefa = st.session_state.editando_tarefa
    opcoes_disciplina_nomes = [""] + list(st.session_state.mapa_disc_id.keys())

    disciplina_atual_nome = ""
    if tarefa.get("disciplinaId"):
        disciplina_atual_nome = st.session_state.mapa_id_disc.get(tarefa.get("disciplinaId"), "")

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

                novo_disciplina_id = st.session_state.mapa_disc_id.get(nova_disciplina_nome)
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