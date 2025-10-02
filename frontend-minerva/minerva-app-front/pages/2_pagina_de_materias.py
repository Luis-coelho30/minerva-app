import streamlit as st
from utils import setup_logged
from menu import menu_with_redirect

st.set_page_config(page_title="Materias", page_icon="./images/Minerva_logo.jpeg", layout="wide")   # define qual nome a aba vai ter no navegador

largura_logo_home = 150

setup_logged()  # define a cor de fundo e que a pagina comeca mais pra cima pra logo ficar mais alta

menu_with_redirect()

with st.expander(icon=":material/add:",label="Criar nova materia"):
     with st.form("nova_disciplina_form", clear_on_submit=True):
        nome = st.text_input("Nome da Disciplina")
        descricao = st.text_area("Descrição (Opcional)")
        media_necessaria = st.number_input("Média Necessária para Aprovação", min_value=0.0, max_value=10.0, value=7.0, step=0.5)
        faltas = st.number_input("Faltas até agora", min_value=0, step=1)
        creditos = st.number_input("Créditos", min_value=0, step=1, format="%d")
        
        enviado = st.form_submit_button("Adicionar Disciplina")
        # envia os dados pro banco de dados
st.markdown("---")

# pegar as disciplinas do BD e mostrar

# exemplo
for n in range(10):
    with st.container(border=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader("Disciplina de Exemplo ")
            st.write(f"**Créditos:** N/A | **Média Necessária:** N/A")

        
    

    