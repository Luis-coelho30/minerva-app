import streamlit as st
from menu import menu
from utils import initialize_session_state

initialize_session_state()

# Initialize st.session_state.role to None
if "role" not in st.session_state:
    st.session_state.role = None
if "_role" not in st.session_state:
    st.session_state._role = None

# Retrieve the role from Session State to initialize the widget
st.session_state._role = st.session_state.role

menu()  # Render the dynamic menu!
if st.session_state.role is None:
    st.switch_page("pages/pagina_de_abertura.py")
