import streamlit as st
from dataset import df
from utils import format_number
from transformacoes import receita_por_estado
from graficos import grafico_receita_estado

st.set_page_config(
    page_title="Dashboard de Vendas",
    layout="wide"
)

st.markdown("""
<style>
div[data-testid="stMetric"] {
    background-color: #F4F6F9;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #E0E0E0;
}

div[data-testid="stMetricLabel"] {
    font-size: 20px !important;
    font-weight: 600 !important;
    color: #555555;
}

div[data-testid="stMetricValue"] {
    font-size: 34px !important;
    font-weight: 700 !important;
    color: #1F5DA8;
}
</style>
""", unsafe_allow_html=True)


st.title("Dashboard de Vendas \U0001F6D2")

df_rec_estado = receita_por_estado(df)

aba_dataset, aba_receita, aba_vendedores = st.tabs(
    ['\U0001F4C4 Dataset', '\U0001F4B0 Receita', '\U0001F464 Vendedores']
)

# ================= DATASET =================
with aba_dataset:
    st.subheader("Visualização do Dataset")
    st.dataframe(df, use_container_width=True)

# ================= RECEITA =================
with aba_receita:

    coluna1, coluna2 = st.columns(2)

    with coluna1:
        st.metric(
            '\U0001F4B0 Receita Total',
            format_number(df['Preço'].sum(), prefix='R$ ')
        )

    with coluna2:
        st.metric(
            '\U0001F4E6 Quantidade de Vendas',
            format_number(df.shape[0])
        )

    st.divider()

    st.markdown("### \U0001F4CA Visão Executiva de Performance Comercial")

    st.plotly_chart(
        grafico_receita_estado(df_rec_estado),
        use_container_width=True
    )
