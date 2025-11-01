import streamlit as st
from typing import Callable


def disciplina_component(disciplina: dict,
                         on_editar: Callable,
                         on_arquivar: Callable,
                         on_excluir: Callable,
                         on_att_faltas: Callable,
                         add_nota_ui: Callable,
                         mostrar_notas_ui: Callable
                         ):

    with st.container(border=True):
        col_info, col_botoes = st.columns([5, 1], gap="small")

        with col_info:
            st.subheader(disciplina.get("nome", "Nome não informado"))

            carga_horaria = disciplina.get("cargaHorariaTotal", 0)
            duracao_aula = disciplina.get("cargaHorariaAula", 1)
            faltas_registradas = disciplina.get("faltasRegistradas", 0)

            limite_total_aulas = 0
            if duracao_aula > 0:
                limite_total_aulas = int((carga_horaria * 0.25) // duracao_aula)

            faltas_restantes = limite_total_aulas - faltas_registradas

            media_atual = disciplina.get('mediaAtual')
            media_formatada = f"{media_atual:.2f}" if isinstance(media_atual, (int, float)) else "N/A"

            st.write(
                f"**Créditos:** {disciplina.get('creditos', 'N/A')} | "
                f"**Média:** {media_formatada} (de {disciplina.get('mediaNecessaria', 'N/A')}) | "
            )

            # Cria duas colunas, uma com o form de faltas e outra vazia para diminuir o espaço ocupado
            col_form_container, _1, _2 = st.columns(3)

            with col_form_container:
                with st.form(key=f"form_faltas_{disciplina.get('id')}", clear_on_submit=False):
                    st.write(f"**Faltas:** {faltas_registradas} de {limite_total_aulas} (Restam: {faltas_restantes})")
                    col_input, col_btn = st.columns(2)

                    with col_input:
                        novo_total_faltas = st.number_input(
                            "Faltas:",
                            min_value=0,
                            max_value=limite_total_aulas,
                            value=faltas_registradas,
                            step=1,
                            format="%d",
                            key=f"num_faltas_{disciplina.get('id')}",
                            label_visibility="collapsed"
                        )
                    with col_btn:
                        if st.form_submit_button("Salvar", use_container_width=True):
                            on_att_faltas(disciplina, novo_total_faltas)

            st.divider()

            disciplina_id = disciplina.get("id")
            add_nota_ui(disciplina_id)
            mostrar_notas_ui(disciplina_id)

        with col_botoes:
            st.button("Editar",
                      key=f"edit_disc_{disciplina.get('id')}",
                      on_click=on_editar,
                      args=(disciplina,),
                      use_container_width=True)

            with st.popover("Arquivar", use_container_width=True):
                st.write(f"Tem certeza que deseja arquivar '{disciplina.get('nome')}'?")
                st.button("Confirmar",
                          type="primary",
                          key=f"confirm_archive_{disciplina.get('id')}",
                          on_click=on_arquivar,
                          args=(disciplina,))

            with st.popover("Excluir", use_container_width=True):
                st.markdown(
                    f"Tem certeza que deseja excluir **'{disciplina.get('nome')}'** permanentemente?\n\n"
                    "Isso também apagará as notas, tarefas e arquivos associados."
                )
                st.button("Confirmar Exclusão",
                          type="primary",
                          key=f"confirm_delete_active_disc_{disciplina.get('id')}",
                          on_click=on_excluir,
                          args=(disciplina,))


def disciplina_arquivada_component(
        disciplina: dict,
        on_desarquivar: Callable,
        on_excluir: Callable
):
    with st.container(border=True):
        col1, col2, col3 = st.columns([4, 1, 1])

        with col1:
            st.subheader(f"*(Arquivada)* {disciplina.get('nome', 'Nome não informado')}")

        with col2:
            st.button("Desarquivar",
                      key=f"unarchive_{disciplina.get('id')}",
                      on_click=on_desarquivar,
                      args=(disciplina,),
                      use_container_width=True)

        with col3:
            with st.popover("Excluir", use_container_width=True):
                st.write(f"Tem certeza que deseja excluir '{disciplina.get('nome')}' permanentemente?")
                st.button("Confirmar Exclusão",
                          type="primary",
                          key=f"confirm_delete_archived_disc_{disciplina.get('id')}",
                          on_click=on_excluir,
                          args=(disciplina,))