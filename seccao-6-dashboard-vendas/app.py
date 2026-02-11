import streamlit as st
import plotly.express as px
from dataset import df
from utils import format_number

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

with aba_receita:
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.metric(
            'Receita Total',
            format_number(df['Preço'].sum(), prefix='R$')
        )
    with coluna2:
        st.metric('Quantidade de Vendas', format_number(df.shape[0]))