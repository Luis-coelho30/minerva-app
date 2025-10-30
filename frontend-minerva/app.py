import streamlit as st
from menu import menu
from api_client.client import ApiClient
from api_client.endpoints.UserEndpoint import UserEndpoint
from api_client.endpoints.TaskEndpoint import TaskEndpoint
from api_client.endpoints.DisciplineEndpoint import DisciplinaEndpoint
from api_client.endpoints.GradeEndpoint import GradeEndpoint
from api_client.endpoints.FileEndpoint import FileEndpoint

# Initialize st.session_state.role to None
if "role" not in st.session_state:
    st.session_state.role = None
if "_role" not in st.session_state:
    st.session_state._role = None

# Retrieve the role from Session State to initialize the widget
st.session_state._role = st.session_state.role

def set_role():
    # Callback function to save the role selection to Session State
    st.session_state.role = st.session_state._role

if "client" not in st.session_state:
    client = ApiClient(base_url="http://localhost:8080")
    st.session_state.client = client
    st.session_state.user_api = UserEndpoint(client)
    st.session_state.task_api = TaskEndpoint(client)
    st.session_state.disc_api = DisciplinaEndpoint(client)
    st.session_state.grade_api = GradeEndpoint(client)
    st.session_state.file_api = FileEndpoint(client)


menu() # Render the dynamic menu!
st.switch_page("pages/pagina_de_abertura.py")
