# -*- coding: utf-8 -*-

from pathlib import Path
import streamlit as st
import pandas as pd

# ==================================================
# Constantes de negócio
# ==================================================
PERC_COMISSAO = 0.05

COLUNAS_ANALISE = [
    "loja",
    "vendedor",
    "produto",
    "cliente_genero",
    "forma_pagamento"
]

COLUNAS_NUMERICAS = [
    "preco",
    "comissao"
]

FUNCOES_AGREGACAO = {
    "Soma": "sum",
    "Contagem": "count"
}

# ==================================================
# Configuração de caminhos
# ==================================================
BASE_DIR = Path(__file__).parent
DATASET_DIR = BASE_DIR / "datasets"

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
    left=df_compras,
    right=df_produtos[["produto", "preco"]],
    on="produto",
    how="left"
)

# Retorna data como índice
df_compras = df_compras.set_index("data")

# Calcula comissão
df_compras["comissao"] = df_compras["preco"] * PERC_COMISSAO

# ==================================================
# Função de formatação monetária (APENAS VISUAL)
# ==================================================
def formatar_real(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# ==================================================
# Interface – Streamlit
# ==================================================
st.title("📊 Tabela Dinâmica de Vendas")

st.sidebar.header("Configurações")

indice_dinamico = st.sidebar.multiselect(
    "Selecione os índices (linhas)",
    COLUNAS_ANALISE
)

colunas_disponiveis = [c for c in COLUNAS_ANALISE if c not in indice_dinamico]

coluna_dinamica = st.sidebar.multiselect(
    "Selecione as colunas",
    colunas_disponiveis
)

valor_analise = st.sidebar.selectbox(
    "Selecione o valor",
    COLUNAS_NUMERICAS
)

metrica_analise = st.sidebar.selectbox(
    "Selecione a métrica",
    list(FUNCOES_AGREGACAO.keys())
)

# ==================================================
# Criação da Tabela Dinâmica
# ==================================================
if indice_dinamico and coluna_dinamica:
    metrica = FUNCOES_AGREGACAO[metrica_analise]

    compras_dinamica = pd.pivot_table(
        df_compras,
        index=indice_dinamico,
        columns=coluna_dinamica,
        values=valor_analise,
        aggfunc=metrica,
        fill_value=0
    )

    # Total por linha
    compras_dinamica["TOTAL_GERAL"] = compras_dinamica.sum(axis=1)

    # Total geral (linha final)
    total_geral = compras_dinamica.sum(axis=0)
    total_geral.name = "TOTAL_GERAL"

    compras_dinamica = pd.concat([compras_dinamica, total_geral.to_frame().T])

    # ==================================================
    # Exibição formatada (R$)
    # ==================================================
    st.dataframe(
        compras_dinamica.style.format(
            {col: formatar_real for col in compras_dinamica.columns}
        )
    )

else:
    st.info("👈 Selecione pelo menos um índice e uma coluna para gerar a tabela.")
