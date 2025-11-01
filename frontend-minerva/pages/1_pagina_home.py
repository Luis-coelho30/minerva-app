import streamlit as st
from streamlit_calendar import calendar as st_calendar
import datetime
from utils import setup_logged, initialize_session_state
from menu import menu_with_redirect
from init_session import ensure_session_state

initialize_session_state()
ensure_session_state()

st.set_page_config(page_title="Home", page_icon="./images/Minerva_logo.jpeg", layout="wide")   # define qual nome a aba vai ter no navegador

largura_logo_home = 150

setup_logged()   # define a cor de fundo e que a pagina comeca mais pra cima pra logo ficar mais alta
menu_with_redirect()

task_api = st.session_state.task_api

st.subheader("Calendário")
if "tarefas" not in st.session_state:
    st.session_state.tarefas = task_api.list_user_tasks()

def formatar_tarefas_para_calendario(tarefas: list):
    eventos_formatados = []
    for tarefa in tarefas:
        titulo = tarefa.get("titulo")
        status = tarefa.get("status")
        arquivada = tarefa.get("arquivada", False)

        data_inicio_str = tarefa.get("dataInicio")
        data_fim_str = tarefa.get("dataFim")

        data_inicio = None
        data_fim = None

        try:
            # Converte as datas das tarefas para o formato usado pelo st_calendar (YYYY-MM-DD)
            if data_inicio_str:
                data_inicio = datetime.datetime.strptime(data_inicio_str, "%d/%m/%Y").strftime("%Y-%m-%d")

            if data_fim_str:
                data_fim = datetime.datetime.strptime(data_fim_str, "%d/%m/%Y").strftime("%Y-%m-%d")

            #Se houver apenas uma data redefine as variáveis para formatar o evento
            if data_fim and not data_inicio:
                data_inicio = data_fim

            if data_inicio and not data_fim:
                data_fim = data_inicio

        except ValueError:
            continue

        # Define a cor baseada no status
        color = "blue"
        if arquivada:
            color = "grey"
        elif status == "Concluída":
            color = "green"
        elif status == "Em Progresso":
            color = "orange"

        # Adiciona o evento formatado para o st_calendar
        if data_inicio and data_fim:
            eventos_formatados.append({
                "title": titulo,
                "start": data_inicio,
                "end": data_fim,
                "color": color,
                "resourceId": "tarefa"
            })

    return eventos_formatados



# Formata as tarefas
lista_de_eventos = formatar_tarefas_para_calendario(st.session_state.tarefas)

# Configura o calendario
calendar_options = {
    "initialView": "dayGridMonth",
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": "dayGridMonth,timeGridWeek,timeGridDay",
    },
    "editable": False,
    "selectable": True
}

calendar = st_calendar(
    events=lista_de_eventos,
    options=calendar_options,
    custom_css="""
    .fc-event-past { opacity: 0.8; }
    .fc-event-time { font-style: italic; }
    .fc-event-title { font-weight: 700; }
    .fc-toolbar-title { font-size: 1.5rem; }
    """
)