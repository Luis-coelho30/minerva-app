import streamlit as st
from typing import Callable


def documento_component(documento: dict, on_editar: Callable, on_excluir: Callable, disciplina_nome: str = ""):


    doc_id = documento.get("id")
    if not doc_id:
        st.error(f"Componente de documento recebeu dados inválidos (sem ID): {documento.get('nomeOriginal')}")
        return

    nome = documento.get("nomeOriginal", "Documento sem nome")
    descricao = documento.get("descricao")
    tipo = documento.get("tipo", "")
    data_upload = documento.get("dataInicio", "")
    url_download = documento.get("url", "#")

    with st.container(border=True):
        col_info, col_botoes = st.columns([5, 1], gap="small")

        with col_info:
            st.subheader(f"{nome}")

            info_linha = []
            if disciplina_nome:
                info_linha.append(f"**{disciplina_nome}**")
            if tipo:
                info_linha.append(f"{tipo}")
            if data_upload:
                info_linha.append(f"{data_upload}")

            if info_linha:
                st.caption(" | ".join(info_linha))

            if descricao:
                st.write(f"{descricao}")

        with col_botoes:
            st.button(
                "Editar",
                icon=":material/edit:",
                key=f"edit_doc_{doc_id}",
                on_click=on_editar,
                args=(documento,),
                use_container_width=True
            )

            st.link_button(
                "Baixar",
                icon=":material/download:",
                url=url_download,
                use_container_width=True,
                disabled=(url_download == "#")
            )

            st.button(
                "Excluir",
                icon=":material/delete:",
                key=f"delete_doc_{doc_id}",
                on_click=on_excluir,
                args=(doc_id,),
                use_container_width=True
            )