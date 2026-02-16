import streamlit as st
import pandas as pd
import altair as alt
from dataset import df


# ==========================================================
# CACHE
# ==========================================================
@st.cache_data
def get_dataframe():
    return df.copy()


# ==========================================================
# TÍTULO
# ==========================================================
st.title("\U0001F4CA Visão Geral de Vendas")
st.divider()

df_base = get_dataframe()

# ==========================================================
# VALIDAÇÃO INICIAL
# ==========================================================
if df_base.empty:
    st.warning("\U000026A0 Dataset vazio.")
    st.stop()

# ==========================================================
# KPIs PRINCIPAIS
# ==========================================================
receita_total = df_base["Preço"].sum()
total_pedidos = df_base.shape[0]
ticket_medio = df_base["Preço"].mean()
frete_total = df_base["Frete"].sum()

st.subheader("\U0001F4C8 Indicadores Principais")

col1, col2, col3, col4 = st.columns(4)

col1.metric("\U0001F4B0 Receita Total", f"R$ {receita_total:,.2f}")
col2.metric("\U0001F4E6 Total de Pedidos", f"{total_pedidos}")
col3.metric("\U0001F9FE Ticket Médio", f"R$ {ticket_medio:,.2f}")
col4.metric("\U0001F69A Frete Total", f"R$ {frete_total:,.2f}")

st.divider()

# ==========================================================
# RECEITA POR CATEGORIA (COM ROTATE NO EIXO X)
# ==========================================================
st.subheader("\U0001F4E6 Receita por Categoria")

receita_categoria = (
    df_base
    .groupby("Categoria do Produto")["Preço"]
    .sum()
    .reset_index()
)

grafico_categoria = alt.Chart(receita_categoria).mark_bar().encode(
    x=alt.X(
        "Categoria do Produto:N",
        sort="-y",
        axis=alt.Axis(labelAngle=-45)
    ),
    y=alt.Y("Preço:Q"),
    tooltip=["Categoria do Produto", "Preço"]
)

st.altair_chart(grafico_categoria, use_container_width=True)

st.divider()

# ==========================================================
# RECEITA MENSAL (COM ROTATE NO EIXO X)
# ==========================================================
st.subheader("\U0001F4C5 Receita Mensal")

df_tempo = df_base.copy()
df_tempo["Mes"] = df_tempo["Data da Compra"].dt.to_period("M")

receita_mensal = (
    df_tempo
    .groupby("Mes")["Preço"]
    .sum()
    .reset_index()
)

receita_mensal["Mes"] = receita_mensal["Mes"].astype(str)

grafico_mensal = alt.Chart(receita_mensal).mark_line(point=True).encode(
    x=alt.X(
        "Mes:N",
        axis=alt.Axis(labelAngle=-45)
    ),
    y=alt.Y("Preço:Q"),
    tooltip=["Mes", "Preço"]
)

st.altair_chart(grafico_mensal, use_container_width=True)

st.divider()

# ==========================================================
# TOP 5 PRODUTOS (COM ROTATE NO EIXO X)
# ==========================================================
st.subheader("\U0001F3C6 Top 5 Produtos por Receita")

top_produtos = (
    df_base
    .groupby("Produto")["Preço"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)

grafico_top = alt.Chart(top_produtos).mark_bar().encode(
    x=alt.X(
        "Produto:N",
        sort="-y",
        axis=alt.Axis(labelAngle=-45)
    ),
    y=alt.Y("Preço:Q"),
    tooltip=["Produto", "Preço"]
)

st.altair_chart(grafico_top, use_container_width=True)
