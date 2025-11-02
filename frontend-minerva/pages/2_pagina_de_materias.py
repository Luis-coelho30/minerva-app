import streamlit as st
from init_session import ensure_session_state
from utils import setup_logged, initialize_session_state
from menu import menu_with_redirect
from components.disciplina_component import disciplina_component, disciplina_arquivada_component
from components.nota_component import nota_component
from pathlib import Path

initialize_session_state()
ensure_session_state()

BASE_DIR = Path(__file__).parent.parent
image_path = BASE_DIR / "images" / "Minerva_logo.jpeg"

st.set_page_config(page_title="Materias", page_icon=image_path, layout="wide")

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

                    if "mapa_de_notas" in st.session_state:
                        del st.session_state.mapa_de_notas

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
        nova_carga_horaria = st.number_input("Carga horária total (em horas)",
                                             min_value=1, step=1, format="%d",
                                             value=disciplina_para_editar.get("cargaHorariaTotal", 1))
        nova_duracao_aula = st.number_input("Duração de uma aula (em horas)",
                                            min_value=1, step=1, format="%d",
                                            value=disciplina_para_editar.get("cargaHorariaAula", 1))

        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Salvar"):

                faltas_atuais = disciplina_para_editar["faltasRegistradas"]

                novo_limite_horas = nova_carga_horaria * 0.25
                novo_limite_aulas = 0
                if nova_duracao_aula > 0:
                    novo_limite_aulas = int(novo_limite_horas // nova_duracao_aula)

                if novo_limite_aulas < faltas_atuais:
                    st.error(
                        f"Erro: O novo limite de faltas ({novo_limite_aulas}) é menor que "
                        f"as faltas já registradas ({faltas_atuais}). "
                        "Ajuste a carga horária ou a duração da aula."
                    )

                if nova_duracao_aula > nova_carga_horaria:
                    st.error(
                        f"Erro: A duração de uma aula é maior que a ({nova_duracao_aula}) "
                        f" carga horária total da disciplina ({nova_carga_horaria}). "
                        "Ajuste a carga horária ou a duração da aula."
                    )

                if nova_duracao_aula > 8:
                    st.error(
                        f"Erro: A duração de uma aula é maior que 8h. "
                        "Tem certeza disso? Ajuste a duração da aula."
                    )

                else:
                    disciplina_editada = {
                        "nome": novo_nome,
                        "descricao": nova_descricao,
                        "arquivada": disciplina_para_editar["arquivada"],
                        "mediaNecessaria": nova_media,
                        "mediaAtual": disciplina_para_editar["mediaAtual"],
                        "creditos": novos_creditos,
                        "cargaHorariaTotal": nova_carga_horaria,
                        "cargaHorariaAula": nova_duracao_aula,
                        "faltasRegistradas": faltas_atuais
                    }

                    try:
                        disc_api.update_discipline(disciplina_para_editar["id"], disciplina_editada)

                        if "lista_de_disciplinas" in st.session_state:
                            del st.session_state.lista_de_disciplinas

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

        if "mapa_de_notas" in st.session_state:
            del st.session_state.mapa_de_notas

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

        if "lista_de_disciplinas" in st.session_state:
            del st.session_state.lista_de_disciplinas

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

        if "lista_de_disciplinas" in st.session_state:
            del st.session_state.lista_de_disciplinas

        st.toast(f"Matéria '{disciplina.get('nome')}' arquivada.")
    except Exception as e:
        st.error(f"Erro ao desarquivar a matéria: {e}")


def handle_excluir_disciplina(disciplina):
    try:
        disc_api.delete_discipline(disciplina.get("id"))

        if "lista_de_disciplinas" in st.session_state:
            del st.session_state.lista_de_disciplinas
        if "mapa_de_notas" in st.session_state:
            del st.session_state.mapa_de_notas

        st.toast(f"Matéria '{disciplina.get("nome")}' excluída!")
    except Exception as e:
        st.error(f"Erro ao excluir a matéria: {e}")


def handle_atualizar_faltas(disciplina, novo_total_faltas):
    try:
        disc_id = disciplina.get('id')
        payload_completo = disciplina.copy()
        if "id" in payload_completo:
            del payload_completo["id"]

        payload_completo.update({
            "faltasRegistradas": novo_total_faltas
        })

        disciplina_atualizada = disc_api.update_discipline(disc_id, payload_completo)

        for i, d in enumerate(st.session_state.lista_de_disciplinas):
            if d.get("id") == disc_id:
                st.session_state.lista_de_disciplinas[i] = disciplina_atualizada
                break

        st.toast("Contagem de faltas atualizada.")
        st.rerun()

    except Exception as e:
        st.error(f"Erro ao atualizar faltas: {e}")


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

                    if "mapa_de_notas" in st.session_state:
                        del st.session_state.mapa_de_notas
                    if "lista_de_disciplinas" in st.session_state:
                        del st.session_state.lista_de_disciplinas

                    st.rerun()
                else:
                    st.warning("Peso deve ser maior que zero e nota deve estar entre 0 e 10.")


def mostrar_notas_ui(disciplina_id: int):
    with st.expander("Ver notas"):
        try:
            lista_de_notas = st.session_state.mapa_de_notas.get(disciplina_id, [])

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
            limite_horas = carga_horaria * 0.25
            limite_aulas = 0

            if duracao_aula > 0:
                limite_aulas = int(limite_horas // duracao_aula)

            if not nome or media_necessaria <= 0.0 or creditos <= 0:
                st.error("Nome, Média (maior que 0) e Créditos (maior que 0) são obrigatórios.")

            if duracao_aula > carga_horaria:
                st.error(
                    f"Erro: A duração de uma aula é maior que a ({duracao_aula}) "
                    f" carga horária total da disciplina ({carga_horaria}). "
                    "Ajuste a carga horária ou a duração da aula."
                )

            if duracao_aula > 8:
                st.error(
                    f"Erro: A duração de uma aula é maior que 8h. "
                    "Tem certeza disso? Ajuste a duração da aula."
                )

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
                    "cargaHorariaTotal": carga_horaria,
                    "cargaHorariaAula": duracao_aula,
                    "faltasRegistradas": 0
                }

                disc_api.create_discipline(disciplina_payload)

                if "lista_de_disciplinas" in st.session_state:
                    del st.session_state.lista_de_disciplinas

                st.success(f"Disciplina '{nome}' criada com sucesso!")
                st.rerun()
st.markdown("---")

try:
    if "lista_de_disciplinas" not in st.session_state:
        st.session_state.lista_de_disciplinas = disc_api.list_user_discipline()

    if "mapa_de_notas" not in st.session_state:
        st.session_state.mapa_de_notas = nota_api.list_all_user_grades_grouped()
        st.session_state.mapa_de_notas = {int(k): v for k, v in st.session_state.mapa_de_notas.items()}

    lista_de_disciplinas = st.session_state.lista_de_disciplinas
    disciplinas_ativas = [d for d in lista_de_disciplinas if not d.get('arquivada', False)]
    disciplinas_arquivadas = [d for d in lista_de_disciplinas if d.get('arquivada', False)]

    if not disciplinas_ativas:
        st.info("Você ainda não cadastrou nenhuma matéria. Adicione uma acima!")
    else:
        for disciplina in disciplinas_ativas:
            disciplina_component(
                disciplina=disciplina,
                on_editar=handle_iniciar_edicao_disciplina,
                on_arquivar=handle_arquivar_disciplina,
                on_excluir=handle_excluir_disciplina,
                on_att_faltas = handle_atualizar_faltas,
                add_nota_ui=add_nota_ui,
                mostrar_notas_ui=mostrar_notas_ui,
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