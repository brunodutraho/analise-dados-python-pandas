# -*- coding: utf-8 -*-

from pathlib import Path
from datetime import timedelta

import streamlit as st
import pandas as pd

# ==================================================
# Configuração de caminhos
# ==================================================
BASE_DIR = Path(__file__).parent
DATASET_DIR = BASE_DIR / "datasets"

# ==================================================
# Função utilitária – Formatação monetária BR
# ==================================================
def formatar_real(valor: float) -> str:
    """
    Formata valores numéricos no padrão brasileiro:
    R$ 1.000,00
    """
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# ==================================================
# Leitura dos dados
# ==================================================
df_compras = pd.read_csv(
    DATASET_DIR / "compras.csv",
    sep=";",
    decimal=",",
    index_col=0,
    parse_dates=True,
    encoding="utf-8"
)

df_lojas = pd.read_csv(
    DATASET_DIR / "lojas.csv",
    sep=";",
    decimal=",",
    index_col=0,
    encoding="utf-8"
)

df_produtos = pd.read_csv(
    DATASET_DIR / "produtos.csv",
    sep=";",
    decimal=",",
    index_col=0,
    encoding="utf-8"
)

# ==================================================
# Tratamento dos dados
# ==================================================

# Padroniza nome da coluna para merge
df_produtos = df_produtos.rename(columns={"nome": "produto"})

# Remove índice de data para permitir merge
df_compras = df_compras.reset_index()

# Merge com preços dos produtos
df_compras = pd.merge(
    df_compras,
    df_produtos[["produto", "preco"]],
    on="produto",
    how="left"
)

# Retorna data como índice
df_compras = df_compras.set_index("data")

# Calcula comissão (5%)
df_compras["comissao"] = df_compras["preco"] * 0.05

# ==================================================
# Sidebar – Filtro de período
# ==================================================
st.sidebar.header("📅 Filtro de Período")

data_max = df_compras.index.date.max()
data_inicio = st.sidebar.date_input(
    "Data Inicial",
    data_max - timedelta(days=6)
)
data_final = st.sidebar.date_input(
    "Data Final",
    data_max
)

# Aplica filtro
df_filtrado = df_compras[
    (df_compras.index.date >= data_inicio) &
    (df_compras.index.date <= data_final)
]

# ==================================================
# Interface – KPIs Gerais
# ==================================================
st.title("📊 Análise de Volume de Vendas")

st.subheader("Números Gerais")
col1, col2 = st.columns(2)

valor_total = df_filtrado["preco"].sum()
qtd_total = df_filtrado.shape[0]

col1.metric("Valor de compras no período", formatar_real(valor_total))
col2.metric("Quantidade de compras", qtd_total)

st.divider()

# ==================================================
# Análise por Loja
# ==================================================
if not df_filtrado.empty:
    principal_loja = df_filtrado["loja"].value_counts().idxmax()
    df_loja = df_filtrado[df_filtrado["loja"] == principal_loja]

    st.subheader(f"🏬 Principal Loja: {principal_loja}")

    col21, col22 = st.columns(2)
    col21.metric(
        "Valor de compras",
        formatar_real(df_loja["preco"].sum())
    )
    col22.metric(
        "Quantidade de compras",
        df_loja.shape[0]
    )

    st.divider()

    # ==================================================
    # Análise por Vendedor
    # ==================================================
    principal_vendedor = df_filtrado["vendedor"].value_counts().idxmax()
    df_vendedor = df_filtrado[df_filtrado["vendedor"] == principal_vendedor]

    st.subheader(f"🧑‍💼 Principal Vendedor: {principal_vendedor}")

    col31, col32 = st.columns(2)
    col31.metric(
        "Valor de compras",
        formatar_real(df_vendedor["preco"].sum())
    )
    col32.metric(
        "Comissão no período",
        formatar_real(df_vendedor["comissao"].sum())
    )

else:
    st.warning("⚠️ Nenhum dado encontrado para o período selecionado.")
