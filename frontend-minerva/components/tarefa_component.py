import streamlit as st

def tarefa_component(titulo, descricao=None, status="Pendente", disciplina="", prioridade="Média", 
                     arquivada=False, data_inicio=None, data_final=None, concluido_em=None):
    
    with st.container(border=True):
        col1, col2, col3, col4 = st.columns([4, 1, 1, 1])
        
        with col1:
            # Título com ícone de status
            st.subheader(f" {titulo}")
            
            # Linha de informações principais
            info_linha = []
            if disciplina:
                info_linha.append(f"{disciplina}")
            info_linha.append(f"{prioridade}")
            info_linha.append(f"{status}")
            
            st.caption(" | ".join(info_linha))
            
            # Descrição
            if descricao:
                st.write(f"{descricao}")
            
            # Datas
            datas_info = []
            if data_inicio:
                datas_info.append(f"Início: {data_inicio}")
            if data_final:
                datas_info.append(f"Prazo: {data_final}")
            if concluido_em:
                datas_info.append(f"Concluído: {concluido_em}")
            
            if datas_info:
                st.caption(" | ".join(datas_info))
        
        with col2:
            if st.button("Editar", key=f"edit_{titulo}"):
                st.session_state.editando_tarefa = {
                    "titulo": titulo,
                    "descricao": descricao,
                    "status": status,
                    "disciplina": disciplina,
                    "prioridade": prioridade,
                    "data_inicio": data_inicio,
                    "data_final": data_final
                }
        
        with col3:
            if status != "Concluída":
                if st.button("Concluir", key=f"complete_{titulo}"):
                    # Atualizar status da tarefa para concluída
                    for i, t in enumerate(st.session_state.tarefas):
                        if t["titulo"] == titulo:
                            st.session_state.tarefas[i]["status"] = "Concluída"
                            break
                    st.success("Tarefa concluída!")
                    st.rerun()
            else:
                st.write("Concluída")
        
        with col4:
            if st.button("Excluir", key=f"delete_{titulo}"):
                # Remover tarefa da lista
                st.session_state.tarefas = [t for t in st.session_state.tarefas if t["titulo"] != titulo]
                st.success(f"Tarefa '{titulo}' excluída!")
                st.rerun()
    
    pass