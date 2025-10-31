import streamlit as st


def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.page_link("pages/1_pagina_home.py", label="Home", icon=":material/home:")
    st.sidebar.page_link("pages/2_pagina_de_materias.py", label="Materias", icon=":material/book_2:")
    st.sidebar.page_link("pages/3_pagina_de_tarefas.py", label="Tarefas", icon=":material/note_stack:")
    st.sidebar.page_link("pages/4_pagina_de_documentos.py", label="Arquivos", icon=":material/bookmarks:")



def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.page_link("app.py", label="Log in")


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
        st.switch_page("app.py")
    menu()
