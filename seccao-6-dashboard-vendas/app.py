import streamlit as st
from dataset import df
from utils import format_number, load_all_css
from transformacoes import ( 
    receita_por_estado,
    receita_mensal,
    receita_por_categoria,
    performance_vendedores
)
from graficos import (
    grafico_receita_estado,
    grafico_receita_mensal,
    grafico_barra_receita_estado,
    grafico_receita_categoria,
    grafico_receita_vendedores,
    grafico_vendas_vendedores
)

st.set_page_config(
    page_title="Dashboard de Vendas",
    layout="wide"
)

st.markdown(load_all_css(), unsafe_allow_html=True)

st.title("Dashboard de Vendas \U0001F6D2")
st.divider()

df_rec_estado = receita_por_estado(df)
df_rec_mensal = receita_mensal(df)
df_rec_categoria = receita_por_categoria(df)
df_perf = performance_vendedores(df)

df_rec_vendedores = df_perf.sort_values('Receita_Total', ascending=False)
df_vendas_vendedores = df_perf.sort_values('Quantidade_Vendas', ascending=False)


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
     
    coluna3, coluna4 = st.columns(2)
    with coluna3:
        st.subheader("Receita por Estado")
        st.plotly_chart(
            grafico_receita_estado(df_rec_estado),
            use_container_width=True
        )
    with coluna4:
        st.subheader("Receita Mensal")
        st.plotly_chart(
            grafico_receita_mensal(df_rec_mensal),
            use_container_width=True
        )
    coluna5, coluna6 = st.columns(2)
    with coluna5:
        st.subheader("Top 5 Receita por Estados")
        st.plotly_chart(
            grafico_barra_receita_estado(df_rec_estado),
            use_container_width=True
        )

    with coluna6:
        st.subheader("Top 7 Categoria Produto")
        st.plotly_chart(
            grafico_receita_categoria(df_rec_categoria),
            use_container_width=True
        )

with aba_vendedores:
    
    coluna1, coluna2 = st.columns(2)

    with coluna1:
        st.subheader("Top 7 Receita por Vendedores")
        st.plotly_chart(
            grafico_receita_vendedores(df_rec_vendedores),
            use_container_width=True
        )
    
    with coluna2:
        st.subheader("Top 7 Quantidade de Vendas por Vendedores")
        st.plotly_chart(
            grafico_vendas_vendedores(df_vendas_vendedores),
            use_container_width=True
        )