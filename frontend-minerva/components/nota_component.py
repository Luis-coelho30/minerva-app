import streamlit as st
from typing import Callable

def nota_component(nota: dict, disciplina_id: int, on_editar: Callable, on_excluir: Callable):
    with st.container(border=True):
        col1, col2, col3 = st.columns([3, 1, 1])

        with col1:
            valor_nota = nota.get('valor')
            valor_formatado = f"{valor_nota:.2f}" if isinstance(valor_nota, (int, float)) else "N/A"
            st.subheader(nota.get("descricao", "Descrição não informada"))
            st.write(f"**Valor:** {valor_formatado} | **Peso:** {nota.get('peso', 'N/A')}")

        with col2:
            nota_selecionada = {
                "id": nota.get("id"),
                "descricao": nota.get("descricao"),
                "valor": nota.get("valor"),
                "peso": nota.get("peso"),
                "disciplinaId": disciplina_id
            }
            st.button("Editar",
                      key=f"edit_nota_{nota.get('id')}",
                      on_click=on_editar,
                      args=(nota_selecionada,),
                      use_container_width=True)

        with col3:
            with st.popover("Excluir", use_container_width=True):
                st.write(f"Tem certeza que deseja excluir a nota '{nota.get('descricao')}'?")
                st.button("Confirmar Exclusão",
                          type="primary",
                          key=f"confirm_delete_nota_{nota.get('id')}",
                          on_click=on_excluir,
                          args=(nota,))