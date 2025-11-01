import streamlit as st
from init_session import ensure_session_state
from utils import setup_logged, initialize_session_state
from menu import menu_with_redirect
from components.disciplina_component import disciplina_component, disciplina_arquivada_component
from components.nota_component import nota_component

initialize_session_state()
ensure_session_state()

st.set_page_config(page_title="Materias", page_icon="./images/Minerva_logo.jpeg", layout="wide")

setup_logged()
menu_with_redirect()

disc_api = st.session_state.disc_api
nota_api = st.session_state.grade_api

@st.dialog("Modificar Nota")
def editar_nota_dialog(nota_para_editar):
    with st.form("editar_nota_form"):
        st.write("**Modificar nota**")
        nova_desc = st.text_input("Descrição", value=nota_para_editar["descricao"])
        novo_valor = st.number_input("Valor", min_value=0.0, max_value=10.0, step=0.1, value=nota_para_editar["valor"])
        novo_peso = st.number_input("Peso", min_value=1, step=1, format="%d", value=nota_para_editar["peso"])
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Salvar"):
                nota_editada = {
                    "descricao": nova_desc,
                    "valor": round(novo_valor, 2),
                    "peso": novo_peso,
                    "disciplinaId": nota_para_editar["disciplinaId"]
                }

                try:
                    nota_api.update_grade(nota_para_editar["id"], nota_editada)
                    st.toast("Nota atualizada com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao atualizar a nota: {e}")
        with col2:
            if st.form_submit_button("Cancelar", type="secondary"):
                st.rerun()


@st.dialog("Modificar Disciplina")
def editar_disciplina_dialog(disciplina_para_editar):
    with st.form("editar_disciplina_form"):
        st.write("**Modificar Disciplina**")
        novo_nome = st.text_input("Nome da Disciplina", value=disciplina_para_editar["nome"])
        nova_descricao = st.text_area("Descrição (Opcional)", value=disciplina_para_editar.get("descricao", ""))
        nova_media = st.number_input("Média Necessária", min_value=0.0, max_value=10.0, step=0.5,
                                     value=disciplina_para_editar["mediaNecessaria"])
        novos_creditos = st.number_input("Créditos", min_value=1, step=1, format="%d",
                                         value=disciplina_para_editar["creditos"])
        nova_carga_horaria = st.number_input("Carga horária total (em horas)", min_value=1, step=1, format="%d")
        nova_duracao_aula = st.number_input("Duração de uma aula (em horas)", min_value=1, step=1, format="%d")

        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Salvar"):

                limite_de_horas = nova_carga_horaria * 0.25
                limite_aulas = int(limite_de_horas // nova_duracao_aula)

                disciplina_editada = {
                    "nome": novo_nome,
                    "descricao": nova_descricao,
                    "arquivada": disciplina_para_editar["arquivada"],
                    "mediaNecessaria": nova_media,
                    "mediaAtual": disciplina_para_editar["mediaAtual"],
                    "creditos": novos_creditos,
                    "faltasRestantes": limite_aulas
                }

                try:
                    disc_api.update_discipline(disciplina_para_editar["id"], disciplina_editada)
                    st.toast("Disciplina atualizada com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao atualizar a disciplina: {e}")
        with col2:
            if st.form_submit_button("Cancelar", type="secondary"):
                st.rerun()


def handle_iniciar_edicao_nota(nota_selecionada):
    editar_nota_dialog(nota_selecionada)


def handle_excluir_nota(nota):
    try:
        nota_api.delete_grade(nota.get("id"))
        st.toast(f"Nota '{nota.get("descricao")}' excluída!")
    except Exception as e:
        st.error(f"Erro ao excluir a nota: {e}")


def handle_iniciar_edicao_disciplina(disciplina):
    editar_disciplina_dialog(disciplina)


def handle_arquivar_disciplina(disciplina):
    try:
        disc_id = disciplina.get('id')
        payload_completo = disciplina.copy()
        payload_completo["arquivada"] = True

        if "id" in payload_completo:
            del payload_completo["id"]

        disc_api.update_discipline(disc_id, payload_completo)
        st.toast(f"Matéria '{disciplina.get('nome')}' arquivada.")
    except Exception as e:
        st.error(f"Erro ao arquivar a matéria: {e}")


def handle_desarquivar_disciplina(disciplina):
    try:
        disc_id = disciplina.get("id")
        payload_completo = disciplina.copy()
        payload_completo["arquivada"] = False

        if "id" in payload_completo:
            del payload_completo["id"]

        disc_api.update_discipline(disc_id, payload_completo)
        st.toast(f"Matéria '{disciplina.get('nome')}' arquivada.")
    except Exception as e:
        st.error(f"Erro ao desarquivar a matéria: {e}")


def handle_excluir_disciplina(disciplina):
    try:
        disc_api.delete_discipline(disciplina.get("id"))
        st.toast(f"Matéria '{disciplina.get("nome")}' excluída!")
    except Exception as e:
        st.error(f"Erro ao excluir a matéria: {e}")


def add_nota_ui(disciplina_id: int):
    with st.expander(icon=":material/add:", label="Adicionar nota"):
        with st.form(f"form_nota_{disciplina_id}", clear_on_submit=True):
            st.write("**Adicionar nova nota**")
            cols_form = st.columns([2, 1, 1])
            with cols_form[0]:
                desc_nota = st.text_input("Descrição da Nota (Ex: P1, A1)")
            with cols_form[1]:
                valor_nota = st.number_input("Valor", min_value=0.0, max_value=10.0, step=0.1)
            with cols_form[2]:
                peso_nota = st.number_input("Peso", min_value=1, step=1, format="%d")

            if st.form_submit_button("Adicionar Nota"):
                if desc_nota and peso_nota > 0 and 0.0 <= valor_nota <= 10.0:
                    nota_payload = {
                        "descricao": desc_nota,
                        "valor": round(valor_nota, 2),
                        "peso": peso_nota,
                        "disciplinaId": disciplina_id
                    }

                    nota_api.create_grade(nota_payload)
                    st.rerun()
                else:
                    st.warning("Peso deve ser maior que zero e nota deve estar entre 0 e 10.")


def mostrar_notas_ui(disciplina_id: int):
    with st.expander("Ver notas"):
        try:
            lista_de_notas = nota_api.list_grades_by_discipline(disciplina_id)
            if not lista_de_notas:
                st.info("Você ainda não cadastrou nenhuma nota na matéria. Adicione uma acima!")
            else:
                for nota in lista_de_notas:
                    nota_component(
                        nota=nota,
                        disciplina_id=disciplina_id,
                        on_editar=handle_iniciar_edicao_nota,
                        on_excluir=handle_excluir_nota
                    )
        except Exception as e:
            st.error(f"Não foi possível carregar as notas. Erro: {e}")


with st.expander(icon=":material/add:", label="Criar nova materia"):
    with st.form("nova_disciplina_form", clear_on_submit=True):
        nome = st.text_input("Nome da Disciplina")
        descricao = st.text_area("Descrição (Opcional)")
        media_necessaria = st.number_input("Média Necessária", min_value=0.0, max_value=10.0, value=7.0, step=0.5)
        creditos = st.number_input("Créditos", min_value=1, step=1, format="%d")
        carga_horaria = st.number_input("Carga horária total (em horas)", min_value=1, step=1, format="%d")
        duracao_aula = st.number_input("Duração de uma aula (em horas)", min_value=1, step=1, format="%d")

        enviado = st.form_submit_button("Adicionar Disciplina")
        if enviado:
            if not nome or media_necessaria <= 0.0 or creditos <= 0:
                st.error("Nome, Média (maior que 0) e Créditos (maior que 0) são obrigatórios.")
            else:
                limite_de_horas = carga_horaria * 0.25
                limite_aulas = int(limite_de_horas // duracao_aula)

                disciplina_payload = {
                    "nome": nome,
                    "descricao": descricao,
                    "arquivada": False,
                    "mediaNecessaria": media_necessaria,
                    "mediaAtual": 0.0,
                    "creditos": creditos,
                    "faltasRestantes": limite_aulas
                }

                disc_api.create_discipline(disciplina_payload)
                st.success(f"Disciplina '{nome}' criada com sucesso!")
                st.rerun()
st.markdown("---")

try:
    lista_de_disciplinas = disc_api.list_user_discipline()
    disciplinas_ativas = [d for d in lista_de_disciplinas if not d.get('arquivada', False)]
    disciplinas_arquivadas = [d for d in lista_de_disciplinas if d.get('arquivada', False)]

    if not disciplinas_ativas:
        st.info("Você ainda não cadastrou nenhuma matéria. Adicione uma acima!")
    else:
        # Loop de Disciplinas Ativas
        for disciplina in disciplinas_ativas:
            # Chama o componente "burro" de disciplina
            disciplina_component(
                disciplina=disciplina,
                on_editar=handle_iniciar_edicao_disciplina,
                on_arquivar=handle_arquivar_disciplina,
                on_excluir=handle_excluir_disciplina,
                add_nota_ui=add_nota_ui,          # Passa a função de UI
                mostrar_notas_ui=mostrar_notas_ui
            )

    if disciplinas_arquivadas:
        with st.expander("Matérias Arquivadas"):
            for disciplina in disciplinas_arquivadas:
                disciplina_arquivada_component(
                    disciplina=disciplina,
                    on_desarquivar=handle_desarquivar_disciplina,
                    on_excluir=handle_excluir_disciplina
                )
except Exception as e:
    st.error(f"Não foi possível carregar as disciplinas. Erro: {e}")