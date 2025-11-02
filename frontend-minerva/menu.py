import streamlit as st

from pathlib import Path

BASE_DIR = Path(__file__).parent
pagina_home_path = BASE_DIR / "pages" / "1_pagina_home.py"
pagina_de_materias_path = BASE_DIR / "pages" / "2_pagina_de_materias.py"
pagina_de_tarefas_path = BASE_DIR / "pages" / "3_pagina_de_tarefas.py"
pagina_de_documentos_path = BASE_DIR / "pages" / "4_pagina_de_documentos.py"
app_path = BASE_DIR / "app.py"

def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.page_link(pagina_home_path, label="Início", icon=":material/home:")
    st.sidebar.page_link(pagina_de_materias_path, label="Materias", icon=":material/book_2:")
    st.sidebar.page_link(pagina_de_tarefas_path, label="Tarefas", icon=":material/note_stack:")
    st.sidebar.page_link(pagina_de_documentos_path, label="Arquivos", icon=":material/bookmarks:")



def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.page_link(app_path, label="Log in")


def menu():
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        unauthenticated_menu()
        return
    authenticated_menu()


def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        st.switch_page(app_path)
    menu()
