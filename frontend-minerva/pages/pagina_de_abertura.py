import streamlit as st
def pagina_de_abertura():
    st.title("🎓Minerva")    
    st.write("Bem vindo ao app de organização academica!")
    if st.button("Entrar"):
        st.switch_page("pagina_de_login.py")
    
    st.button("Cadastrar")