import streamlit as st
from utils import setup_logged
from menu import menu_with_redirect
from components import tarefa_component

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("styles/pagina_de_tarefas.css")

@st.dialog("Editar Tarefa")
def editar_tarefa_modal():
    tarefa = st.session_state.editando_tarefa
    
    with st.form("editar_tarefa_form"):
        novo_titulo = st.text_input("Título da Tarefa", value=tarefa["titulo"])
        nova_descricao = st.text_area("Descrição", value=tarefa["descricao"] or "")
        novo_status = st.selectbox("Status", ["Pendente", "Em Progresso", "Concluída", "Cancelada"], 
                                  index=["Pendente", "Em Progresso", "Concluída", "Cancelada"].index(tarefa["status"]))
        nova_disciplina = st.text_input("Disciplina", value=tarefa["disciplina"])
        nova_prioridade = st.selectbox("Prioridade", ["Baixa", "Média", "Alta"], 
                                      index=["Baixa", "Média", "Alta"].index(tarefa["prioridade"]))
        
        # Converter strings de data para objetos date se existirem
        data_inicio_value = None
        if tarefa["data_inicio"]:
            from datetime import datetime
            data_inicio_value = datetime.strptime(tarefa["data_inicio"], "%Y-%m-%d").date()
        
        data_final_value = None
        if tarefa["data_final"]:
            from datetime import datetime
            data_final_value = datetime.strptime(tarefa["data_final"], "%Y-%m-%d").date()
        
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

st.set_page_config(page_title="Tarefas", page_icon="./images/Minerva_logo.jpeg")   # define qual nome a aba vai ter no navegador

setup_logged()  # define a cor de fundo e que a pagina comeca mais pra cima pra logo ficar mais alta

menu_with_redirect()

if "tarefas" not in st.session_state:
    st.session_state.tarefas = []

with st.expander(icon=":material/add:", label="Adicionar Nova Tarefa", expanded=False):
    with st.form("nova_tarefa_form", clear_on_submit=True):
        titulo = st.text_input("Título da Tarefa")
        descricao = st.text_area("Descrição (Opcional)")
        status = st.selectbox("Status", ["Pendente", "Em Progresso", "Concluída", "Cancelada"])
        disciplina = st.text_input("Disciplina")
        prioridade = st.selectbox("Prioridade", ["Baixa", "Média", "Alta"])
        data_inicio = st.date_input("Data de Início (Opcional)", value=None)
        data_final = st.date_input("Data Final (Opcional)", value=None)
        
        submitted = st.form_submit_button("Adicionar Tarefa")
        
        if submitted and titulo:
            # Criar nova tarefa
            nova_tarefa = {
                "titulo": titulo,
                "descricao": descricao if descricao else None,
                "status": status,
                "disciplina": disciplina,
                "prioridade": prioridade,
                "data_inicio": str(data_inicio) if data_inicio else None,
                "data_final": str(data_final) if data_final else None,
                "concluido_em": None
            }
            
            # Adicionar à lista
            st.session_state.tarefas.append(nova_tarefa)
            st.success(f"Tarefa '{titulo}' adicionada com sucesso!")
            st.rerun()  # Atualizar a página
        elif submitted and not titulo:
            st.error("O título da tarefa é obrigatório!")

st.markdown("---")

# Exibir tarefas
if not st.session_state.tarefas:
    st.success("Ótimo trabalho! Nenhuma tarefa pendente. ✨")
else:
    for tarefa in st.session_state.tarefas:
        tarefa_component(**tarefa)  # Usar ** para passar todos os parâmetros

# Verificar se deve abrir modal de edição
if "editando_tarefa" in st.session_state:
    editar_tarefa_modal()