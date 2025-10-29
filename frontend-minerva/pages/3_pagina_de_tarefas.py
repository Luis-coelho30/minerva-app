import streamlit as st
from utils import setup_logged
from menu import menu_with_redirect

st.set_page_config(page_title="Tarefas", page_icon="./images/Minerva_logo.jpeg")   # define qual nome a aba vai ter no navegador

setup_logged()  # define a cor de fundo e que a pagina comeca mais pra cima pra logo ficar mais alta

menu_with_redirect()

with st.expander(icon=":material/add:", label="Adicionar Nova Tarefa", expanded=False):
    with st.form("nova_tarefa_form", clear_on_submit=True):
        titulo = st.text_input("Título da Tarefa")
        descricao = st.text_area("Descrição (Opcional)")
        # disciplina_id = st.selectbox("Disciplina")
        data_fim = st.date_input("Data de Entrega")
        prioridade = st.selectbox("Prioridade", ["Baixa", "Média", "Alta"])
        
        submitted = st.form_submit_button("Adicionar Tarefa")
        

st.markdown("---")

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