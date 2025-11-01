import streamlit as st
from typing import Callable
import datetime

def tarefa_component(tarefa: dict,
                     on_editar: Callable,
                     on_concluir: Callable,
                     on_excluir: Callable,
                     on_arquivar: Callable
                     ):
    tarefa_id = tarefa.get("id")
    if not tarefa_id:
        st.error(f"Componente de tarefa recebeu dados inválidos (sem ID): {tarefa.get('titulo')}")
        return

    titulo = tarefa.get("titulo", "Tarefa Sem Título")
    descricao = tarefa.get("descricao")
    status = tarefa.get("status", "Pendente")
    disciplina = tarefa.get("disciplina", "")
    prioridade = tarefa.get("prioridade", "Média")
    data_inicio_str = tarefa.get("dataInicio")
    data_final_str = tarefa.get("dataFinal")
    concluido_em_str = tarefa.get("concluido_em")

    hoje = datetime.date.today()
    is_due_soon = False

    if data_final_str and status != "Concluída":
        try:
            data_final_obj = datetime.datetime.strptime(data_final_str, "%d/%m/%Y").date()
            delta = data_final_obj - hoje

            if delta.days <= 7:
                is_due_soon = True

        except ValueError:
            pass

    with st.container(border=True):
        col_info, col_botoes = st.columns([5, 1], gap="small")

        with col_info:
            st.subheader(f"{titulo}")

            info_linha = []
            if disciplina:
                info_linha.append(f"**{disciplina}**")
            info_linha.append(f"{prioridade}")
            info_linha.append(f"{status}")

            st.caption(" | ".join(info_linha))

            if descricao:
                st.write(f"{descricao}")

            datas_info = []
            if data_inicio_str:
                datas_info.append(f"Início: {data_inicio_str}")

            if data_final_str:
                prazo_str = f"Prazo: {data_final_str}"

                if is_due_soon:
                    datas_info.append(f":red[{prazo_str}]")
                else:
                    datas_info.append(prazo_str)

            if concluido_em_str:
                datas_info.append(f"Concluído: {concluido_em_str}")

            if datas_info:
                st.caption(" | ".join(datas_info))

        with col_botoes:
            st.button(
                "✏️ Editar",
                key=f"edit_{tarefa_id}",
                on_click=on_editar,
                args=(tarefa,),
                use_container_width=True
            )

            st.button(
                "✅ Concluir" if status != "Concluída" else "🎉 Concluída",
                key=f"complete_{tarefa_id}",
                on_click=on_concluir,
                args=(tarefa_id,),
                use_container_width=True,
                disabled=(status == "Concluída")
            )

            with st.popover("🗃️ Arquivar", use_container_width=True):
                st.write(f"Tem certeza que deseja arquivar '{titulo}'?")
                st.button("Confirmar",
                          type="primary",
                          key=f"confirm_archive_task_{tarefa_id}",
                          on_click=on_arquivar,
                          args=(tarefa,))

            with st.popover("🗑️ Excluir", use_container_width=True):
                st.write(f"Tem certeza que deseja excluir '{titulo}'?")
                st.button("Confirmar Exclusão",
                          type="primary",
                          key=f"confirm_delete_task_{tarefa_id}",
                          on_click=on_excluir,
                          args=(tarefa_id,))


def tarefa_arquivada_component(tarefa: dict,
                               on_desarquivar: Callable,
                               on_excluir: Callable
                               ):

    tarefa_id = tarefa.get("id")
    titulo = tarefa.get("titulo", "Tarefa Sem Título")

    with st.container(border=True):
        col_info, col_botoes = st.columns([5, 1], vertical_alignment="center", gap="small")

        with col_info:
            st.subheader(f"*(Arquivada)* {titulo}")
            if tarefa.get("disciplina"):
                st.caption(f"**{tarefa.get('disciplina')}**")

        with col_botoes:
            st.button(
                "📤 Desarquivar",
                key=f"unarchive_task_{tarefa_id}",
                on_click=on_desarquivar,
                args=(tarefa,),
                use_container_width=True
            )

            with st.popover("🗑️ Excluir", use_container_width=True):
                st.write(f"Tem certeza que deseja excluir '{titulo}'?")
                st.button("Confirmar Exclusão",
                          type="primary",
                          key=f"confirm_delete_archived_task_{tarefa_id}",
                          on_click=on_excluir,
                          args=(tarefa_id,))