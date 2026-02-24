import streamlit as st
import dados

st.title("Filmes")

nome = st.text_input("Nome do filme:")
ano = st.number_input("Ano de Lançamento:", min_value=2010, max_value=2026, step=1)
nota = st.slider("Nota do filme:", min_value=0.0, max_value=10.0, step=0.1)

# Botão para inserir os dados
if st.button("Cadastrar"):
    dados.insere_dados(nome, ano, nota)
    st.success("Filme cadastrado com sucesso!")

# Listar os dados
filmes = dados.obter_dados()
st.subheader("Lista de Filmes Cadastrados:")
st.table(filmes)
