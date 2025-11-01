import streamlit as st
from typing import Callable


def disciplina_component(disciplina: dict, on_editar: Callable, on_arquivar: Callable, on_excluir: Callable, add_nota_ui: Callable, mostrar_notas_ui: Callable):

    with st.container(border=True):
        col1, col2, col3, col4 = st.columns([4, 1, 1, 1])

        with col1:
            media_atual = disciplina.get('mediaAtual')
            media_formatada = f"{media_atual:.2f}" if isinstance(media_atual, (int, float)) else "N/A"

            st.subheader(disciplina.get("nome", "Nome não informado"))
            st.write(
                f"**Créditos:** {disciplina.get('creditos', 'N/A')} | "
                f"**Média:** {disciplina.get('mediaNecessaria', 'N/A')} | "
                f"**Média atual:** {media_formatada}"
            )

            disciplina_id = disciplina.get("id")
            add_nota_ui(disciplina_id)
            mostrar_notas_ui(disciplina_id)

        with col2:
            st.button("Editar",
                      key=f"edit_disc_{disciplina.get('id')}",
                      on_click=on_editar,
                      args=(disciplina,),
                      use_container_width=True)

        with col3:
            with st.popover("Arquivar", use_container_width=True):
                st.write(f"Tem certeza que deseja arquivar '{disciplina.get('nome')}'?")
                st.button("Confirmar",
                          type="primary",
                          key=f"confirm_archive_{disciplina.get('id')}",
                          on_click=on_arquivar,
                          args=(disciplina,))

        with col4:
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