import streamlit as st
from utils import setup_logged, initialize_session_state
from menu import menu_with_redirect
from init_session import ensure_session_state

initialize_session_state()
ensure_session_state()

st.set_page_config(page_title="Home", page_icon="./images/Minerva_logo.jpeg", layout="wide")   # define qual nome a aba vai ter no navegador

largura_logo_home = 150

setup_logged()   # define a cor de fundo e que a pagina comeca mais pra cima pra logo ficar mais alta

menu_with_redirect()

st.subheader("Calendario") 
st.subheader("Tarefas de Hoje:")
tarefas_pendentes = 1
if not tarefas_pendentes:
    st.success("Ótimo trabalho! Nenhuma tarefa pendente. ✨")
else:
    # Ordenar por prioridade e depois por data
    # prioridade_map = {"Alta": 0, "Média": 1, "Baixa": 2}
    # tarefas_pendentes.sort(key=lambda x: (prioridade_map[x['prioridade']], x['data_fim']))

    for n in range(4):

        with st.container(border=True):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.subheader("Tarefa exemplo")
                st.caption(f"Disciplina: disciplina exemplo | Prioridade: Alta")
                # if tarefa['descricao']:
                #     st.write(tarefa['descricao'])