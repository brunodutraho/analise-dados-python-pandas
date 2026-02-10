import streamlit as st
import plotly.express as px
from dataset import df

st.set_page_config(
    page_title="Dashboard de Vendas",
    layout="wide"
)

st.title("Dashboard de Vendas \U0001F6D2")

aba_dataset, aba_receita, aba_vendedores = st.tabs(
    ['\U0001F4C4 Dataset', '\U0001F4B0 Receita', '\U0001F464 Vendedores']
)

with aba_dataset:
    st.subheader("Visualização do Dataset")
    st.dataframe(df, use_container_width=True)
