from pathlib import Path
from datetime import datetime

import streamlit as st
import pandas as pd

# ==================================================
# Configuração de caminhos
# ==================================================
# BASE_DIR garante que o script funcione corretamente
# independentemente de onde ele é executado
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
    encoding="utf-8"
)

df_produtos = pd.read_csv(
    DATASET_DIR / "produtos.csv",
    sep=";",
    decimal=",",
    encoding="utf-8"
)

# ==================================================
# Preparação dos dados auxiliares
# ==================================================

# Cria coluna combinando cidade e estado
df_lojas["cidade_estado"] = df_lojas["cidade"] + " / " + df_lojas["estado"]

# Lista de lojas
lista_lojas = df_lojas["cidade_estado"].to_list()

# ==================================================
# Sidebar – Entrada de dados
# ==================================================
st.sidebar.header("🛒 Nova Compra")

loja_selecionada = st.sidebar.selectbox(
    "Selecione a loja:",
    lista_lojas
)

# Recupera vendedores da loja selecionada
lista_vendedores = (
    df_lojas.loc[
        df_lojas["cidade_estado"] == loja_selecionada,
        "vendedores"
    ]
    .iloc[0]
    .strip("[]")
    .replace("'", "")
    .split(", ")
)

vendedor_selecionado = st.sidebar.selectbox(
    "Selecione o vendedor:",
    lista_vendedores
)

# Produtos
lista_produtos = df_produtos["nome"].to_list()
produto_selecionado = st.sidebar.selectbox(
    "Selecione o produto:",
    lista_produtos
)

# Cliente
nome_cliente = st.sidebar.text_input("Nome do Cliente")

genero_selecionado = st.sidebar.selectbox(
    "Gênero do Cliente:",
    ["masculino", "feminino"]
)

forma_pagto_selecionado = st.sidebar.selectbox(
    "Forma de Pagamento:",
    ["cartão de crédito", "boleto", "pix", "dinheiro"]
)

# ==================================================
# Ação: adicionar nova compra
# ==================================================
if st.sidebar.button("Adicionar Nova Compra"):
    novo_id = len(df_compras) + 1

    nova_compra = {
        "id_compra": novo_id,
        "loja": loja_selecionada,
        "vendedor": vendedor_selecionado,
        "produto": produto_selecionado,
        "cliente_nome": nome_cliente,
        "cliente_genero": genero_selecionado,
        "forma_pagamento": forma_pagto_selecionado
    }

    df_compras.loc[datetime.now()] = nova_compra

    df_compras.to_csv(
        DATASET_DIR / "compras.csv",
        sep=";",
        decimal=","
    )

    st.success("✅ Compra adicionada com sucesso.")


# ==================================================
# Visualização dos dados
# ==================================================
st.title("📊 Base de Compras")
st.dataframe(df_compras)
