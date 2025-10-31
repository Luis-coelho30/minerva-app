import streamlit as st

def documento_component(nome, descricao=None, disciplina="", tipo="", data_upload=None, arquivo_bytes=None):
    with st.container(border=True):
        col1, col2, col3, col4 = st.columns([4, 1, 1, 1])
        
        with col1:
            # Nome do documento
            st.subheader(f"{nome}")
            
            # Informações principais
            info_linha = []
            if disciplina:
                info_linha.append(f"{disciplina}")
            if tipo:
                info_linha.append(f"{tipo}")
            if data_upload:
                info_linha.append(f"{data_upload}")
            
            if info_linha:
                st.caption(" | ".join(info_linha))
            
            # Descrição
            if descricao:
                st.write(f"{descricao}")
        
        with col2:
            if st.button("Editar", key=f"edit_doc_{nome}"):
                st.session_state.editando_documento = {
                    "nome": nome,
                    "descricao": descricao,
                    "disciplina": disciplina,
                    "tipo": tipo,
                    "data_upload": data_upload,
                    "arquivo_bytes": arquivo_bytes
                }
        
        with col3:
            if arquivo_bytes:
                if st.download_button(
                    label="Baixar",
                    data=arquivo_bytes,
                    file_name=f"{nome}{tipo}",
                    key=f"download_{nome}"
                ):
                    # Limpar modal de edição se estiver aberto
                    if "editando_documento" in st.session_state:
                        del st.session_state.editando_documento
            else:
                st.button("Baixar", key=f"download_{nome}", disabled=True)
        
        with col4:
            if st.button("Excluir", key=f"delete_doc_{nome}"):
                # Limpar modal de edição se estiver aberto
                if "editando_documento" in st.session_state:
                    del st.session_state.editando_documento
                # Remover documento da lista
                st.session_state.documentos = [d for d in st.session_state.documentos if d["nome"] != nome]
                st.success(f"Documento '{nome}' excluído!")
                st.rerun()

@st.dialog("Editar Documento")
def editar_documento_modal():
    doc = st.session_state.editando_documento
    
    with st.form("editar_documento_form"):
        novo_nome = st.text_input("Nome do arquivo", value=doc["nome"])
        nova_descricao = st.text_area("Descrição", value=doc["descricao"] or "")
        nova_disciplina = st.selectbox("Disciplina", options=[1,2], 
                                      index=[1,2].index(int(doc["disciplina"])) if doc["disciplina"].isdigit() else 0)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Salvar"):
                # Atualizar documento na lista
                for i, d in enumerate(st.session_state.documentos):
                    if d["nome"] == doc["nome"]:
                        st.session_state.documentos[i].update({
                            "nome": novo_nome,
                            "descricao": nova_descricao,
                            "disciplina": str(nova_disciplina)
                        })
                        break
                del st.session_state.editando_documento
                st.success("Documento atualizado!")
                st.rerun()
        
        with col2:
            if st.form_submit_button("Cancelar"):
                del st.session_state.editando_documento
                st.rerun()
