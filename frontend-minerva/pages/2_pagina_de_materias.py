import streamlit as st
from utils import setup_logged
from menu import menu_with_redirect

st.set_page_config(page_title="Materias", page_icon="./images/Minerva_logo.jpeg", layout="wide")   # define qual nome a aba vai ter no navegador

largura_logo_home = 150

setup_logged()  # define a cor de fundo e que a pagina comeca mais pra cima pra logo ficar mais alta

menu_with_redirect()

disciplina_api = st.session_state.disc_api
nota_api = st.session_state.grade_api

def add_nota(disciplina_id: int):
    with st.expander(icon=":material/add:", label="Adicionar nota"):
        with st.form(f"form_nota_{disciplina_id}", clear_on_submit=True):
                st.write("**Adicionar nova nota**")
                cols_form = st.columns([2,1,1])
                with cols_form[0]:
                    desc_nota = st.text_input("Descrição da Nota (Ex: P1, A1)")
                with cols_form[1]:
                    valor_nota = st.number_input("Valor", min_value=0.0, max_value=10.0, step=0.1)
                with cols_form[2]:
                    peso_nota = st.number_input("Peso", min_value=0, step=1, format="%d")

                if st.form_submit_button("Adicionar Nota"):
                    if desc_nota and peso_nota > 0:
                        nota_api.create_grade(desc_nota, valor_nota, peso_nota, disciplina_id)
                        st.rerun()
                    else:
                        st.warning("Descrição e peso (maior que zero) são obrigatórios.")

def mostrar_nota(disciplina_id: int):
    try:
        lista_de_notas = nota_api.list_grades_by_discipline(disciplina_id)
        if not lista_de_disciplinas:
            st.info("Você ainda não cadastrou nenhuma nota na matéria. Adicione uma acima!")
        else:
            # Itera sobre cada dicionário de nota na lista
            for nota in lista_de_notas:
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.subheader(nota.get("descricao", "Descrição não informada"))
                        st.write(f"**Valor** {nota.get('valor', 'N/A')} | **Peso:** {nota.get('peso', 'N/A')}")
    except Exception as e:
        st.error(f"Não foi possível carregar as disciplinas. Erro: {e}")

with st.expander(icon=":material/add:",label="Criar nova materia"):
     with st.form("nova_disciplina_form", clear_on_submit=True):
        nome = st.text_input("Nome da Disciplina")
        descricao = st.text_area("Descrição (Opcional)")
        arquivada = False
        media_necessaria = st.number_input("Média Necessária para Aprovação", min_value=0.0, max_value=10.0, value=7.0, step=0.5)
        faltas = st.number_input("Faltas até agora", min_value=0, step=1)
        creditos = st.number_input("Créditos", min_value=0, step=1, format="%d")
        
        enviado = st.form_submit_button("Adicionar Disciplina")
        if enviado:
            if nome is "":
                st.error("Nome é um campo obrigatório")
            elif media_necessaria is 0.0:
                st.error("Média deve ser maior que 0")
            elif creditos is 0:
                st.error("Créditos deve ser maior que 0")
            else:
                disciplina_api.create_discipline(nome, descricao, arquivada, media_necessaria, creditos)
                st.success(f"Disciplina '{nome}' criada com sucesso!")
                st.rerun()
st.markdown("---")

# Pega as disciplinas do banco de dados e as exibe
try:
    lista_de_disciplinas = disciplina_api.list_user_discipline()
    if not lista_de_disciplinas:
        st.info("Você ainda não cadastrou nenhuma matéria. Adicione uma acima!")
    else:
        # Itera sobre cada dicionário de disciplina na lista
        for disciplina in lista_de_disciplinas:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.subheader(disciplina.get("nome", "Nome não informado"))
                    st.write(
                        f"**Créditos:** {disciplina.get('creditos', 'N/A')} | "
                        f"**Média Necessária:** {disciplina.get('mediaNecessaria', 'N/A')} | "
                        f"**Média atual**: {disciplina.get('media_atual', 'N/A')}"
                    )
                    add_nota(disciplina.get("id"))
                    mostrar_nota(disciplina.get("id"))
except Exception as e:
    st.error(f"Não foi possível carregar as disciplinas. Erro: {e}")
    
