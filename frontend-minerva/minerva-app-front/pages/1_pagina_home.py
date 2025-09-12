import streamlit as st
largura_logo_home = 150

# st.markdown(
#     """
#     <style>
#         /* Reduz o padding no topo do container principal */
#         .block-container {
#             padding-top: 1rem; /* Ajuste este valor para mais ou menos espaço */
#         }
#         .stApp {
#             background-color: #112236
#         }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

st.set_page_config(page_title="Home", page_icon="./images/Minerva_logo.jpeg")


col1, mid, col2 = st.columns([1, 10, 1])
with mid:
    col_logo, col_nome = st.columns([1, 3])
    with col_logo:
        st.image("./images/Minerva_logo.jpeg", width= largura_logo_home)            
    with col_nome:
        st.title("Minerva")