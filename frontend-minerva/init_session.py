import streamlit as st

def ensure_session_state():
    if "role" not in st.session_state:
        st.session_state.role = "logado"
    if "_role" not in st.session_state:
        st.session_state._role = "logado"