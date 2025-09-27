import streamlit as st
from utils import setup_logged_css
from menu import menu_with_redirect

if "nome_da_materia_atual" not in st.session_state:
    nome_da_materia = "Materia"
else:
    nome_da_materia = st.session_state.nome_da_materia_atual

setup_logged_css() # define a cor do fundo e tira a sidebar

largura_logo_home = 150

st.set_page_config(page_title=nome_da_materia, page_icon="./images/Minerva_logo.jpeg")   # define qual nome a aba vai ter no navegador

menu_with_redirect()

col1, mid, col2 = st.columns([1, 10, 1])    # coloca a logo e o nome no topo da pagina
with mid:
    col_logo, col_nome = st.columns([1, 3])
    with col_logo:
        st.image("./images/Minerva_logo.jpeg", width= largura_logo_home)            
    with col_nome:
        st.title("Minerva")

st.title(nome_da_materia)
st.subheader("Conteudo da materia:")
st.subheader("Tarefas:")
st.button("Tarefa 1")
st.subheader("Calculadora de media final:")
colPesoA1, colA1, colPesoP1, colP1, colA2, colP2 = st.columns([1, 1, 1, 1, 1, 1])
with colPesoA1:
    pesoA = st.number_input("Peso das atv", min_value=0.0, format="%.2f")
with colA1:
    notaA1 = st.number_input("Nota A1", min_value=0.0, format="%.2f")
with colPesoP1:
    pesoP = st.number_input("Peso das provas", min_value=0.0, format="%.2f")
with colP1:
    notaP1 = st.number_input("Nota P1", min_value=0.0, format="%.2f")
with colA2:
    notaA2 = st.number_input("Nota A2", min_value=0.0, format="%.2f")
with colP2:
    notaP2 = st.number_input("Nota P2", min_value=0.0, format="%.2f")

if st.button("Calcular"):
    denominador = (2 * pesoP) + (2 * pesoA)
    if denominador > 0:
        numerador = (pesoA * notaA1) + (pesoP * notaP1) + (pesoA * notaA2) + (pesoP * notaP2)
        media_final = numerador / denominador
        st.success(f"Sua média final é: {media_final:.2f}")
    else:
        st.error("A soma dos pesos não pode ser zero.")